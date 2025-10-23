"""Обработчики привычек."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from ..states import Habits
from ..texts import texts
from ..keyboards import get_habits_keyboard, get_main_menu, get_cancel_keyboard, kb_post_flow
from ..storage import db
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("habits")
router = Router()


@router.message(F.text == texts.BUTTON_HABITS)
async def cmd_habits(message: Message, state: FSMContext):
    """Обработчик кнопки 'Привычки'."""
    user_id = message.from_user.id
    
    # Получаем привычки пользователя
    async with db._connection.execute("""
        SELECT name, streak FROM habits WHERE tg_id = ? ORDER BY streak DESC
    """, (user_id,)) as cursor:
        habits = await cursor.fetchall()
    
    if not habits:
        await message.answer(
            ux.compose(
                ux.h1("Привычки", "🔥"),
                ux.p("У тебя пока нет привычек. Давай добавим первую!")
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Добавить привычку", callback_data="habit:add")]
                ]
            )
        )
    else:
        habits_text = "\n".join([f"• {h[0]} ({h[1]} дней)" for h in habits])
        await message.answer(
            ux.compose(
                ux.h1("Твои привычки", "🔥"),
                ux.p(habits_text)
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Добавить", callback_data="habit:add")],
                    [InlineKeyboardButton(text="✅ Отметить", callback_data="habit:tick")],
                    [InlineKeyboardButton(text="✏️ Переименовать", callback_data="habit:rename")],
                    [InlineKeyboardButton(text="🗑 Удалить", callback_data="habit:delete")]
                ]
            )
        )


@router.callback_query(F.data == "habit:add")
async def process_habit_add_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка добавления привычки."""
    user_id = callback.from_user.id
    
    # Проверяем лимит привычек для Free плана
    user = await db.get_user(user_id)
    if user and user.plan_tier == "free":
        # Подсчитываем количество привычек
        async with db._connection.execute("""
            SELECT COUNT(*) FROM habits WHERE tg_id = ?
        """, (user_id,)) as cursor:
            count = await cursor.fetchone()
            if count[0] >= 2:
                await callback.message.edit_text(
                    ux.compose(
                        ux.h1("Лимит привычек", "🔥"),
                        ux.p("На бесплатном тарифе можно создать только 2 привычки."),
                        ux.p("Обновите подписку для большего количества привычек.")
                    )
                )
                await callback.answer()
                return
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Добавить привычку", "➕"),
            ux.p("Какую привычку хочешь развивать?")
        )
    )
    await state.set_state(Habits.add)
    await callback.answer()


@router.message(Habits.add)
async def process_add_habit(message: Message, state: FSMContext):
    """Обрабатывает добавление привычки."""
    user_id = message.from_user.id
    habit_name = message.text.strip()
    
    if not habit_name:
        await message.answer("Введите название привычки:")
        return
    
    # Проверяем лимит привычек для Free плана
    user = await db.get_user(user_id)
    if user and user.plan_tier == "free":
        # Подсчитываем количество привычек
        async with db._connection.execute("""
            SELECT COUNT(*) FROM habits WHERE tg_id = ?
        """, (user_id,)) as cursor:
            count = await cursor.fetchone()
            if count[0] >= 2:
                await message.answer(
                    ux.compose(
                        ux.h1("Лимит привычек", "🔥"),
                        ux.p("На бесплатном тарифе можно создать только 2 привычки."),
                        ux.p("Обновите подписку для большего количества привычек.")
                    )
                )
                await state.clear()
                return
    
    # Добавляем привычку
    await db.tick_habit(user_id, habit_name)
    
    # Финальное сообщение
    await message.answer(
        ux.compose(
            ux.h1("Готово", "✅"),
            ux.p(f"Привычка '{habit_name}' добавлена! Я всё запомнил.")
        )
    )
    await state.clear()


@router.callback_query(F.data == "habit:tick")
async def process_habit_tick_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка отметки привычки."""
    user_id = callback.from_user.id
    
    # Получаем привычки пользователя
    async with db._connection.execute("""
        SELECT name, streak FROM habits WHERE tg_id = ? ORDER BY streak DESC
    """, (user_id,)) as cursor:
        habits = await cursor.fetchall()
    
    if not habits:
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Нет привычек", "🔥"),
                ux.p("У тебя пока нет привычек для отметки.")
            )
        )
        await callback.answer()
        return
    
    # Создаем кнопки для выбора привычки
    buttons = []
    for i, (name, streak) in enumerate(habits):
        buttons.append([InlineKeyboardButton(
            text=f"{name} ({streak} дней)", 
            callback_data=f"habit:tick:{i}"
        )])
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Отметить привычку", "✅"),
            ux.p("Какую привычку выполнил?")
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("habit:tick:"))
async def process_habit_tick_select(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора привычки для отметки."""
    user_id = callback.from_user.id
    habit_idx = int(callback.data.split(":")[2])
    
    # Получаем привычки пользователя
    async with db._connection.execute("""
        SELECT name, streak FROM habits WHERE tg_id = ? ORDER BY streak DESC
    """, (user_id,)) as cursor:
        habits = await cursor.fetchall()
    
    if habit_idx < len(habits):
        habit_name = habits[habit_idx][0]
        new_streak = await db.tick_habit(user_id, habit_name)
        
        # Финальное сообщение
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p(f"Привычка '{habit_name}' отмечена! Streak: {new_streak} дней.")
            )
        )
    
    await callback.answer()


@router.callback_query(F.data == "habit:rename")
async def process_habit_rename_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка переименования привычки."""
    user_id = callback.from_user.id
    
    # Получаем привычки пользователя
    async with db._connection.execute("""
        SELECT name, streak FROM habits WHERE tg_id = ? ORDER BY streak DESC
    """, (user_id,)) as cursor:
        habits = await cursor.fetchall()
    
    if not habits:
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Нет привычек", "🔥"),
                ux.p("У тебя пока нет привычек для переименования.")
            )
        )
        await callback.answer()
        return
    
    # Создаем кнопки для выбора привычки
    buttons = []
    for i, (name, streak) in enumerate(habits):
        buttons.append([InlineKeyboardButton(
            text=f"{name} ({streak} дней)", 
            callback_data=f"habit:rename:{i}"
        )])
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Переименовать привычку", "✏️"),
            ux.p("Какую привычку хочешь переименовать?")
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("habit:rename:"))
async def process_habit_rename_select(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора привычки для переименования."""
    user_id = callback.from_user.id
    habit_idx = int(callback.data.split(":")[2])
    
    # Получаем привычки пользователя
    async with db._connection.execute("""
        SELECT name, streak FROM habits WHERE tg_id = ? ORDER BY streak DESC
    """, (user_id,)) as cursor:
        habits = await cursor.fetchall()
    
    if habit_idx < len(habits):
        old_name = habits[habit_idx][0]
        await state.update_data(old_habit_name=old_name)
        await state.set_state(Habits.rename)
        
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Переименовать привычку", "✏️"),
                ux.p(f"Текущее название: {old_name}"),
                ux.p("Введи новое название:")
            )
        )
    
    await callback.answer()


@router.message(Habits.rename)
async def process_habit_rename_text(message: Message, state: FSMContext):
    """Обработка текстового ввода нового названия привычки."""
    user_id = message.from_user.id
    new_name = message.text.strip()
    data = await state.get_data()
    old_name = data.get('old_habit_name')
    
    if not new_name:
        await message.answer("Введите новое название привычки:")
        return
    
    # Обновляем название в БД
    async with db._connection.execute("""
        UPDATE habits SET name = ? WHERE tg_id = ? AND name = ?
    """, (new_name, user_id, old_name)):
        pass
    
    # Сообщение А (финал без кнопок)
    await message.answer(
        ux.compose(
            ux.h1("Готово", "✅"),
            ux.p(f"Привычка переименована: '{old_name}' → '{new_name}'.")
        )
    )
    
    await state.clear()


@router.callback_query(F.data == "habit:delete")
async def process_habit_delete_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка удаления привычки."""
    user_id = callback.from_user.id
    
    # Получаем привычки пользователя
    async with db._connection.execute("""
        SELECT name, streak FROM habits WHERE tg_id = ? ORDER BY streak DESC
    """, (user_id,)) as cursor:
        habits = await cursor.fetchall()
    
    if not habits:
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Нет привычек", "🔥"),
                ux.p("У тебя пока нет привычек для удаления.")
            )
        )
        await callback.answer()
        return
    
    # Создаем кнопки для выбора привычки
    buttons = []
    for i, (name, streak) in enumerate(habits):
        buttons.append([InlineKeyboardButton(
            text=f"{name} ({streak} дней)", 
            callback_data=f"habit:delete:{i}"
        )])
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Удалить привычку", "🗑"),
            ux.p("Какую привычку хочешь удалить?")
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("habit:delete:"))
async def process_habit_delete_select(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора привычки для удаления."""
    user_id = callback.from_user.id
    habit_idx = int(callback.data.split(":")[2])
    
    # Получаем привычки пользователя
    async with db._connection.execute("""
        SELECT name, streak FROM habits WHERE tg_id = ? ORDER BY streak DESC
    """, (user_id,)) as cursor:
        habits = await cursor.fetchall()
    
    if habit_idx < len(habits):
        habit_name = habits[habit_idx][0]
        
        # Удаляем привычку из БД
        async with db._connection.execute("""
            DELETE FROM habits WHERE tg_id = ? AND name = ?
        """, (user_id, habit_name)):
            pass
        
        # Сообщение А (финал без кнопок)
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p(f"Привычка '{habit_name}' удалена.")
            )
        )
        
    
    await callback.answer()