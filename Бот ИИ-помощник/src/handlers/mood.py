"""Обработчики настроения."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime

from ..states import Mood
from ..services import ux, flow
from ..keyboards import kb_post_flow, kb_cancel_reply, kb_mood_energy, kb_mood_feel, kb_mood_note, get_main_menu
from ..texts import texts
from ..storage import db
from ..logger import get_logger

logger = get_logger("mood")
router = Router()


@router.message(F.text.in_({"😊 Настроение", "/mood"}))
async def mood_start(msg: Message, state: FSMContext):
    """Начало опроса настроения."""
    await state.set_state(Mood.energy)
    # await msg.answer_sticker(texts.STICKER_ENERGY)  # Временно отключено
    await msg.answer(
        ux.compose(
            ux.h1("Настроение", "😊"),
            ux.p(texts.MOOD_ENERGY_TITLE)
        ),
        reply_markup=kb_mood_energy()
    )


@router.callback_query(F.data.startswith("mood:energy:"))
async def process_mood_energy(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора энергии."""
    energy = int(callback.data.split(":")[2])
    await state.update_data(energy=energy)
    await state.set_state(Mood.mood)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настроение", "😊"),
            ux.p(texts.MOOD_FEEL_TITLE)
        ),
        reply_markup=kb_mood_feel()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("mood:feel:"))
async def process_mood_feel(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора настроения."""
    mood = int(callback.data.split(":")[2])
    await state.update_data(mood=mood)
    await state.set_state(Mood.note)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настроение", "😊"),
            ux.p(texts.MOOD_NOTE_TITLE)
        ),
        reply_markup=kb_mood_note()
    )
    await callback.answer()


@router.callback_query(F.data == "mood:note:add")
async def process_mood_note_add(callback: CallbackQuery, state: FSMContext):
    """Переход к вводу заметки."""
    await state.set_state(Mood.note_text)
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настроение", "😊"),
            ux.p("Напиши заметку о своём настроении:")
        )
    )
    await callback.answer()


@router.callback_query(F.data == "mood:note:skip")
async def process_mood_note_skip(callback: CallbackQuery, state: FSMContext):
    """Пропуск заметки."""
    await save_mood_and_finish(callback, state, note="")


@router.message(Mood.note_text)
async def process_mood_note_text(msg: Message, state: FSMContext):
    """Обработка введённой заметки."""
    note = msg.text.strip()
    await save_mood_and_finish(msg, state, note=note)


async def save_mood_and_finish(message_or_callback, state: FSMContext, note: str = ""):
    """Сохранение настроения и завершение."""
    data = await state.get_data()
    energy = int(data.get("energy", 0))
    mood = int(data.get("mood", 0))
    
    # Получаем ID пользователя
    if isinstance(message_or_callback, Message):
        user_id = message_or_callback.from_user.id
    else:
        user_id = message_or_callback.from_user.id
    
    # Проверяем, существует ли пользователь в базе
    user = await db.get_user(user_id)
    if not user:
        from ..storage import User
        from datetime import datetime, timedelta
        
        new_user = User(
            tg_id=user_id,
            created_at=datetime.now(),
            plan_tier="free",
            subscription_until=None,
            trial_until=datetime.now() + timedelta(days=3),
            tz="Europe/Moscow",
            morning_hour=8,
            evening_hour=20,
            language="ru",
            persona="mentor",
            ref_code=None,
            ref_count=0
        )
        await db.upsert_user(new_user)

    # Сохраняем настроение
    await db.save_mood(
        tg_id=user_id,
        energy=energy,
        mood=mood,
        note=note
    )

    # Микро-совет на основе оценки
    tip_lines = []
    if energy <= 4 or mood <= 4:
        tip_lines.append("Сделай короткий перерыв и подыши 2 минуты.")
    elif energy >= 8 and mood >= 8:
        tip_lines.append("Отличная динамика — используй фокус-сессию 25 минут.")
    else:
        tip_lines.append("Хорошее состояние — продолжай в том же духе.")

    # Сообщение А (финал без кнопок)
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p("Настроение сохранено! Я всё запомнил.")
            )
        )
    else:
        await message_or_callback.message.edit_text(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p("Настроение сохранено! Я всё запомнил.")
            )
        )
        await message_or_callback.answer()

    # Сообщение B (действия с кнопками)
    if tip_lines:
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(
                ux.compose(
                    ux.h1("Совет на сейчас", "🧘"),
                    ux.p("\n".join(tip_lines))
                ),
                reply_markup=kb_post_flow()
            )
        else:
            await message_or_callback.message.answer(
                ux.compose(
                    ux.h1("Совет на сейчас", "🧘"),
                    ux.p("\n".join(tip_lines))
                ),
                reply_markup=kb_post_flow()
            )

    await state.clear()


# Обработчики для кнопок в kb_post_flow
@router.callback_query(F.data == "focus:open")
async def process_focus_from_mood(callback: CallbackQuery, state: FSMContext):
    """Переход к фокус-сессии из настроения."""
    from .focus import focus_start
    await focus_start(callback.message, state)
    await callback.answer()


@router.callback_query(F.data == "nav:stats")
async def process_stats_from_mood(callback: CallbackQuery, state: FSMContext):
    """Показать статистику дня из настроения."""
    user_id = callback.from_user.id
    
    # Получаем данные за сегодня
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Получаем записи настроения
    async with db._connection.execute("""
        SELECT energy, mood, note FROM mood WHERE tg_id = ? AND date = ?
    """, (user_id, today)) as cursor:
        mood_data = await cursor.fetchone()
    
    # Получаем фокус-сессии
    async with db._connection.execute("""
        SELECT COUNT(*), SUM(duration) FROM pomodoro 
        WHERE tg_id = ? AND DATE(started_at) = ?
    """, (user_id, today)) as cursor:
        focus_data = await cursor.fetchone()
    
    # Получаем привычки
    async with db._connection.execute("""
        SELECT COUNT(*) FROM habits WHERE tg_id = ?
    """, (user_id,)) as cursor:
        habits_count = await cursor.fetchone()
    
    # Формируем статистику
    stats_parts = []
    
    if mood_data:
        stats_parts.append(f"Энергия: {mood_data[0]}/10")
        stats_parts.append(f"Настроение: {mood_data[1]}/10")
        if mood_data[2]:
            stats_parts.append(f"Заметка: {mood_data[2][:50]}...")
    
    if focus_data and focus_data[0] > 0:
        stats_parts.append(f"Фокус-сессий: {focus_data[0]}")
        stats_parts.append(f"Время фокуса: {focus_data[1] or 0} мин")
    
    if habits_count and habits_count[0] > 0:
        stats_parts.append(f"Привычек: {habits_count[0]}")
    
    if not stats_parts:
        stats_text = "Пока нет данных за сегодня"
    else:
        stats_text = "\n".join(stats_parts)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Статистика дня", "📊"),
            ux.p(stats_text)
        ),
        reply_markup=kb_post_flow()
    )
    await callback.answer()