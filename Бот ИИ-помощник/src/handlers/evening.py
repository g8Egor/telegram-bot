"""Обработчики вечернего опроса."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import Evening
from ..texts import texts
from ..keyboards import get_main_menu, kb_evening_done, kb_evening_not_done, kb_evening_learning, kb_post_flow
from ..storage import db
from ..services.gpt import gpt_service
from ..services.memories import memory_service
from ..services.emotion import emotion_service
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("evening")
router = Router()


# Callback обработчики для кнопочного интерфейса
@router.callback_query(F.data.startswith("evening:done:"))
async def process_evening_done_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора выполненных задач через кнопки."""
    done_idx = callback.data.split(":")[2]
    
    if done_idx == "custom":
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Вечерние итоги", "🌙"),
                ux.p("Что удалось сделать сегодня? (через запятую):")
            )
        )
        await state.set_state(Evening.done_text)
    else:
        # Выбираем из пресетов
        done = texts.EVENING_DONE_PRESETS[int(done_idx)]
        await state.update_data(done=[done])
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Вечерние итоги", "🌙"),
                ux.p("Что не получилось?")
            ),
            reply_markup=kb_evening_not_done()
        )
        await state.set_state(Evening.not_done)
    
    await callback.answer()


@router.message(Evening.done_text)
async def process_evening_done_text(message: Message, state: FSMContext):
    """Обработка текстового ввода выполненных задач."""
    done_tasks = [task.strip() for task in message.text.replace('\n', ',').split(',') if task.strip()]
    await state.update_data(done=done_tasks)
    await message.answer(
        ux.compose(
            ux.h1("Вечерние итоги", "🌙"),
            ux.p("Что не получилось?")
        ),
        reply_markup=kb_evening_not_done()
    )
    await state.set_state(Evening.not_done)


@router.message(Evening.done)
async def process_evening_done(message: Message, state: FSMContext):
    """Обрабатывает выполненные задачи."""
    # Парсим список выполненных задач
    done_tasks = [task.strip() for task in message.text.replace('\n', ',').split(',') if task.strip()]
    await state.update_data(done=done_tasks)
    
    await message.answer(texts.EVENING_NOT_DONE)
    await state.set_state(Evening.not_done)


# Callback обработчики для невыполненных задач
@router.callback_query(F.data.startswith("evening:not_done:"))
async def process_evening_not_done_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора невыполненных задач через кнопки."""
    not_done_idx = callback.data.split(":")[2]
    
    if not_done_idx == "custom":
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Вечерние итоги", "🌙"),
                ux.p("Что не получилось? (через запятую):")
            )
        )
        await state.set_state(Evening.not_done_text)
    else:
        # Выбираем из пресетов
        not_done = texts.EVENING_NOT_DONE_PRESETS[int(not_done_idx)]
        await state.update_data(not_done=[not_done])
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Вечерние итоги", "🌙"),
                ux.p("Чему научился сегодня?")
            ),
            reply_markup=kb_evening_learning()
        )
        await state.set_state(Evening.learning)
    
    await callback.answer()


@router.message(Evening.not_done_text)
async def process_evening_not_done_text(message: Message, state: FSMContext):
    """Обработка текстового ввода невыполненных задач."""
    not_done_tasks = [task.strip() for task in message.text.replace('\n', ',').split(',') if task.strip()]
    await state.update_data(not_done=not_done_tasks)
    await message.answer(
        ux.compose(
            ux.h1("Вечерние итоги", "🌙"),
            ux.p("Чему научился сегодня?")
        ),
        reply_markup=kb_evening_learning()
    )
    await state.set_state(Evening.learning)


@router.message(Evening.not_done)
async def process_evening_not_done(message: Message, state: FSMContext):
    """Обрабатывает невыполненные задачи."""
    # Парсим список невыполненных задач
    not_done_tasks = [task.strip() for task in message.text.replace('\n', ',').split(',') if task.strip()]
    await state.update_data(not_done=not_done_tasks)
    
    await message.answer(texts.EVENING_LEARNING)
    await state.set_state(Evening.learning)


# Callback обработчики для обучения
@router.callback_query(F.data.startswith("evening:learning:"))
async def process_evening_learning_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора обучения через кнопки."""
    learning_idx = callback.data.split(":")[2]
    
    if learning_idx == "custom":
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Вечерние итоги", "🌙"),
                ux.p("Чему научился сегодня? (свой вариант):")
            )
        )
        await state.set_state(Evening.learning_text)
    else:
        # Выбираем из пресетов
        learning = texts.EVENING_LEARNING_PRESETS[int(learning_idx)]
        await state.update_data(learning=learning)
        
        # Завершаем вечерний опрос
        await finish_evening_flow(callback, state)
    
    await callback.answer()


@router.message(Evening.learning_text)
async def process_evening_learning_text(message: Message, state: FSMContext):
    """Обработка текстового ввода обучения."""
    learning = message.text
    await state.update_data(learning=learning)
    
    # Завершаем вечерний опрос
    await finish_evening_flow(message, state)


@router.message(Evening.learning)
async def process_evening_learning(message: Message, state: FSMContext):
    """Обрабатывает изученное за день."""
    learning = message.text
    await state.update_data(learning=learning)
    
    # Завершаем вечерний опрос
    await finish_evening_flow(message, state)


async def finish_evening_flow(message_or_callback, state: FSMContext):
    """Завершение вечернего потока."""
    # Получаем все данные
    data = await state.get_data()
    
    # Получаем ID пользователя
    if isinstance(message_or_callback, Message):
        user_id = message_or_callback.from_user.id
    else:
        user_id = message_or_callback.from_user.id
    
    # Получаем пользователя и его персону
    user = await db.get_user(user_id)
    if not user:
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(texts.ERROR_NOT_FOUND)
        else:
            await message_or_callback.message.edit_text(texts.ERROR_NOT_FOUND)
        return
    
    # Получаем контекст из памяти
    memories = await memory_service.get_recent_memories(user_id, 3)
    
    # Генерируем рефлексию через GPT
    reflection = await gpt_service.reflect_evening(
        done=data.get('done', []),
        not_done=data.get('not_done', []),
        learning=data.get('learning', ''),
        persona=user.persona,
        memories=memories
    )
    
    # Сохраняем запись в БД
    await db.save_entry(
        tg_id=user_id,
        entry_type="evening",
        data={
            "done": data.get('done', []),
            "not_done": data.get('not_done', []),
            "learning": data.get('learning', '')
        }
    )
    
    # Добавляем в память
    await memory_service.add_memory(
        tg_id=user_id,
        kind="evening",
        content=f"Вечерняя рефлексия: выполнено {len(data.get('done', []))}, не выполнено {len(data.get('not_done', []))}"
    )
    
    # Сообщение А (финал без кнопок)
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p("Итоги дня сохранены! Я всё запомнил.")
            )
        )
    else:
        await message_or_callback.message.edit_text(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p("Итоги дня сохранены! Я всё запомнил.")
            )
        )
    
    # Сообщение B (действия с кнопками)
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            ux.compose(
                ux.h1("Что дальше?", "🌙"),
                ux.p("Отличная работа! Что планируешь дальше?")
            ),
            reply_markup=kb_post_flow()
        )
    else:
        await message_or_callback.message.answer(
            ux.compose(
                ux.h1("Что дальше?", "🌙"),
                ux.p("Отличная работа! Что планируешь дальше?")
            ),
            reply_markup=kb_post_flow()
        )
    
    await state.clear()