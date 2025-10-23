"""Обработчики фокус-сессий."""
import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from ..states import Focus
from ..texts import texts
from ..keyboards import kb_focus_duration, kb_focus_controls, kb_focus_reflection, kb_post_flow, get_main_menu
from .. import storage
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("focus")
router = Router()

# Хранилище активных сессий
active_sessions = {}

async def start_focus_timer(user_id: int, duration: int, message):
    """Запуск таймера фокус-сессии."""
    import asyncio
    from datetime import datetime, timedelta
    
    # Получаем или создаем время окончания
    if user_id in active_sessions and 'end_time' in active_sessions[user_id]:
        end_time = active_sessions[user_id]['end_time']
    else:
        # Создаем новое время окончания
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration)
        if user_id in active_sessions:
            active_sessions[user_id]['end_time'] = end_time
    
    last_time_str = ""
    
    # Основной цикл таймера
    while user_id in active_sessions and active_sessions[user_id].get("status") == "running":
        now = datetime.now()
        
        # Проверяем, не истекло ли время
        if now >= end_time:
            await complete_focus_session(user_id, message)
            break
        
        # Вычисляем оставшееся время
        remaining = end_time - now
        minutes = int(remaining.total_seconds() // 60)
        seconds = int(remaining.total_seconds() % 60)
        current_time_str = f"{minutes:02d}:{seconds:02d}"
        
        # Обновляем сообщение только если время изменилось
        if current_time_str != last_time_str:
            try:
                await message.edit_text(
                    ux.compose(
                        ux.h1("Фокус-сессия", "🎯"),
                        ux.p(f"Задача: {active_sessions[user_id].get('task', 'Не указана')}"),
                        ux.p(f"⏰ Осталось: {current_time_str}"),
                        ux.p("Сосредоточься на задаче!")
                    ),
                    reply_markup=kb_focus_controls()
                )
                last_time_str = current_time_str
            except Exception as e:
                logger.error(f"Error updating timer: {e}")
                # Если ошибка, продолжаем без обновления сообщения
                pass
        
        await asyncio.sleep(1)  # Обновляем каждую секунду

async def complete_focus_session(user_id: int, message):
    """Завершение фокус-сессии."""
    if user_id in active_sessions:
        session = active_sessions[user_id]
        actual_duration = (datetime.now() - session['started_at']).total_seconds() / 60
        
        # Сохраняем в БД
        await storage.db.log_pomodoro(
            tg_id=user_id,
            started_at=session['started_at'],
            finished_at=datetime.now(),
            duration=int(actual_duration),
            status="completed"
        )
        
        # Удаляем из активных
        del active_sessions[user_id]
        
        # Обновляем сообщение
        await message.edit_text(
            ux.compose(
                ux.h1("Фокус-сессия завершена!", "✅"),
                ux.p(f"Отлично! Ты сфокусировался {int(actual_duration)} минут."),
                ux.p("Время для короткого перерыва!")
            )
        )


@router.message(F.text.in_({"🎯 Фокус-сессия", "/focus"}))
@router.callback_query(F.data == "focus:open")
async def focus_start(msg_or_callback, state: FSMContext):
    """Начало фокус-сессии."""
    logger.info(f"Focus session handler triggered by user {msg_or_callback.from_user.id if hasattr(msg_or_callback, 'from_user') else 'unknown'}")
    logger.info(f"Message type: {type(msg_or_callback)}")
    logger.info(f"Message text: {getattr(msg_or_callback, 'text', 'N/A')}")
    await state.set_state(Focus.selecting)
    
    try:
        # Создаем клавиатуру напрямую
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🍅 25 минут", callback_data="focus:start:25")],
                [InlineKeyboardButton(text="🔥 45 минут", callback_data="focus:start:45")],
                [InlineKeyboardButton(text="❌ Отмена", callback_data="focus:cancel")]
            ]
        )
        
        if isinstance(msg_or_callback, Message):
            await msg_or_callback.answer(
                ux.compose(
                    ux.h1("Фокус-сессия", "🎯"),
                    ux.p("Выбери длительность сессии:")
                ),
                reply_markup=keyboard
            )
        else:
            await msg_or_callback.message.edit_text(
                ux.compose(
                    ux.h1("Фокус-сессия", "🎯"),
                    ux.p("Выбери длительность сессии:")
                ),
                reply_markup=keyboard
            )
            await msg_or_callback.answer()
        logger.info("Focus session interface sent successfully")
    except Exception as e:
        logger.error(f"Error in focus_start: {e}")
        if isinstance(msg_or_callback, Message):
            await msg_or_callback.answer("Ошибка при запуске фокус-сессии")
        else:
            await msg_or_callback.answer("Ошибка при запуске фокус-сессии")


@router.callback_query(F.data.startswith("focus:start:"))
async def process_focus_start(callback: CallbackQuery, state: FSMContext):
    """Начало фокус-сессии."""
    logger.info(f"Focus start callback received: {callback.data} from user {callback.from_user.id}")
    try:
        duration = int(callback.data.split(":")[2])
        logger.info(f"Focus session duration selected: {duration} minutes for user {callback.from_user.id}")
        
        await state.update_data(duration=duration)
        await state.set_state(Focus.task)
        
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Фокус-сессия", "🎯"),
                ux.p(f"Выбрано: {duration} минут"),
                ux.p("Опиши задачу, над которой будешь работать:")
            )
        )
        await callback.answer()
        logger.info("Focus session task prompt sent successfully")
    except Exception as e:
        logger.error(f"Error in process_focus_start: {e}")
        await callback.answer("Ошибка при запуске фокус-сессии")


@router.callback_query(F.data == "focus:cancel")
async def focus_cancel(callback: CallbackQuery, state: FSMContext):
    """Отмена фокус-сессии."""
    await state.clear()
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Отменено", "❌"),
            ux.p("Фокус-сессия отменена. Готов продолжить, когда будешь готов.")
        )
    )
    await callback.answer()


@router.message(Focus.task)
async def process_focus_task(message: Message, state: FSMContext):
    """Обработка задачи для фокус-сессии."""
    task = message.text
    await state.update_data(task=task)
    await state.set_state(Focus.running)
    
    # Сохраняем сессию как активную
    user_id = message.from_user.id
    data = await state.get_data()
    duration = data.get('duration', 25)
    
    active_sessions[user_id] = {
        'started_at': datetime.now(),
        'duration': duration,
        'task': task,
        'status': 'running'
    }
    
    # Отправляем сообщение с таймером
    timer_msg = await message.answer(
        ux.compose(
            ux.h1("Фокус-сессия", "🎯"),
            ux.p(f"Задача: {task}"),
            ux.p(f"⏰ Осталось: {duration:02d}:00"),
            ux.p("Сосредоточься на задаче!")
        ),
        reply_markup=kb_focus_controls()
    )
    
    # Запускаем таймер в фоне
    import asyncio
    asyncio.create_task(start_focus_timer(user_id, duration, timer_msg))


@router.callback_query(F.data == "focus:pause")
async def process_focus_pause(callback: CallbackQuery, state: FSMContext):
    """Пауза фокус-сессии."""
    user_id = callback.from_user.id
    if user_id in active_sessions:
        active_sessions[user_id]['status'] = 'paused'
        # Сохраняем оставшееся время
        session = active_sessions[user_id]
        if 'end_time' in session:
            session['paused_at'] = datetime.now()
            session['remaining_on_pause'] = session['end_time'] - session['paused_at']
        
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Фокус-сессия", "⏸️"),
                ux.p("Сессия на паузе. Нажми 'Продолжить' когда будешь готов.")
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="▶️ Продолжить", callback_data="focus:resume")],
                    [InlineKeyboardButton(text="✅ Готово", callback_data="focus:done")]
                ]
            )
        )
    await callback.answer()


@router.callback_query(F.data == "focus:resume")
async def process_focus_resume(callback: CallbackQuery, state: FSMContext):
    """Продолжение фокус-сессии."""
    user_id = callback.from_user.id
    if user_id in active_sessions:
        session = active_sessions[user_id]
        
        # Восстанавливаем время окончания
        if 'paused_at' in session and 'remaining_on_pause' in session:
            session['end_time'] = datetime.now() + session['remaining_on_pause']
            del session['paused_at']
            del session['remaining_on_pause']
        
        # Устанавливаем статус "running"
        session['status'] = 'running'
        
        duration = session.get('duration', 25)
        task = session.get('task', 'Не указана')
        
        # Показываем текущее оставшееся время
        if 'end_time' in session:
            now = datetime.now()
            remaining = session['end_time'] - now
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
        else:
            time_str = f"{duration:02d}:00"
        
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Фокус-сессия", "🎯"),
                ux.p(f"Задача: {task}"),
                ux.p(f"⏰ Осталось: {time_str}"),
                ux.p("Сосредоточься на задаче!")
            ),
            reply_markup=kb_focus_controls()
        )
        
        # Перезапускаем таймер
        import asyncio
        asyncio.create_task(start_focus_timer(user_id, duration, callback.message))
    await callback.answer()


@router.callback_query(F.data == "focus:stop")
async def process_focus_stop(callback: CallbackQuery, state: FSMContext):
    """Остановка фокус-сессии."""
    user_id = callback.from_user.id
    if user_id in active_sessions:
        session = active_sessions[user_id]
        duration = (datetime.now() - session['started_at']).total_seconds() / 60
        
        # Сохраняем сессию в БД
        await db.log_pomodoro(
            tg_id=user_id,
            duration=int(duration),
            status="stopped"
        )
        
        del active_sessions[user_id]
    
    # Сообщение А (финал без кнопок)
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Фокус-сессия", "⏹️"),
            ux.p("Сессия остановлена. Хорошая работа!")
        )
    )
    
    
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "focus:done")
async def process_focus_done(callback: CallbackQuery, state: FSMContext):
    """Завершение фокус-сессии."""
    user_id = callback.from_user.id
    data = await state.get_data()
    duration = data.get('duration', 25)
    
    if user_id in active_sessions:
        session = active_sessions[user_id]
        actual_duration = (datetime.now() - session['started_at']).total_seconds() / 60
        
        # Сохраняем сессию в БД
        await storage.db.log_pomodoro(
            tg_id=user_id,
            started_at=session['started_at'],
            finished_at=datetime.now(),
            duration=int(actual_duration),
            status="completed"
        )
        
        del active_sessions[user_id]
    
    # Сообщение А (финал без кнопок)
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Фокус-сессия", "✅"),
            ux.p(f"Отлично! {duration} минут фокуса завершены.")
        )
    )
    
    
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "focus:cancel")
async def process_focus_cancel(callback: CallbackQuery, state: FSMContext):
    """Отмена фокус-сессии."""
    user_id = callback.from_user.id
    if user_id in active_sessions:
        del active_sessions[user_id]
    
    await state.clear()
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Главное меню", "🏠"),
            ux.p("Выбери раздел:")
        ),
        reply_markup=get_main_menu()
    )
    await callback.answer()