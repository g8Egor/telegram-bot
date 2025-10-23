"""Обработчики утреннего опроса."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import Morning
from ..texts import texts
from ..keyboards import get_main_menu, get_energy_keyboard, kb_morning_goal, kb_morning_tasks, kb_morning_energy, kb_post_flow
from ..storage import db
from ..services.gpt import gpt_service
from ..services.memories import memory_service
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("morning")
router = Router()


# Callback обработчики для кнопочного интерфейса
@router.callback_query(F.data.startswith("morning:goal:"))
async def process_morning_goal_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора цели через кнопки."""
    goal_idx = callback.data.split(":")[2]
    
    if goal_idx == "custom":
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Утренний план", "🌅"),
                ux.p("Напиши свою цель на сегодня:")
            )
        )
        await state.set_state(Morning.goal_text)
    else:
        # Выбираем из пресетов
        goal = texts.MORNING_GOAL_PRESETS[int(goal_idx)]
        await state.update_data(goal=goal)
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Утренний план", "🌅"),
                ux.p("Отлично! Теперь выбери топ-3 задачи:")
            ),
            reply_markup=kb_morning_tasks()
        )
        await state.set_state(Morning.top3)
    
    await callback.answer()


@router.message(Morning.goal_text)
async def process_morning_goal_text(message: Message, state: FSMContext):
    """Обработка текстового ввода цели."""
    await state.update_data(goal=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Утренний план", "🌅"),
            ux.p("Отлично! Теперь выбери топ-3 задачи:")
        ),
        reply_markup=kb_morning_tasks()
    )
    await state.set_state(Morning.top3)


@router.message(Morning.goal)
async def process_morning_goal(message: Message, state: FSMContext):
    """Обрабатывает главную цель дня."""
    await state.update_data(goal=message.text)
    await message.answer(texts.MORNING_TOP3)
    await state.set_state(Morning.top3)


# Callback обработчики для задач
@router.callback_query(F.data.startswith("morning:task:"))
async def process_morning_task_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора задач через кнопки."""
    task_idx = callback.data.split(":")[2]
    
    if task_idx == "add":
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Утренний план", "🌅"),
                ux.p("Добавь свои задачи (через запятую):")
            )
        )
        await state.set_state(Morning.top3_text)
    else:
        # Выбираем из пресетов
        task = texts.MORNING_TASKS_PRESETS[int(task_idx)]
        await state.update_data(top3=[task])
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Утренний план", "🌅"),
                ux.p("Отлично! Теперь оцени свою энергию:")
            ),
            reply_markup=kb_morning_energy()
        )
        await state.set_state(Morning.energy)
    
    await callback.answer()


@router.message(Morning.top3_text)
async def process_morning_top3_text(message: Message, state: FSMContext):
    """Обработка текстового ввода задач."""
    priorities = [p.strip() for p in message.text.replace('\n', ',').split(',') if p.strip()]
    await state.update_data(top3=priorities[:3])
    await message.answer(
        ux.compose(
            ux.h1("Утренний план", "🌅"),
            ux.p("Отлично! Теперь оцени свою энергию:")
        ),
        reply_markup=kb_morning_energy()
    )
    await state.set_state(Morning.energy)


@router.message(Morning.top3)
async def process_morning_top3(message: Message, state: FSMContext):
    """Обрабатывает топ-3 приоритета."""
    # Парсим список приоритетов (разделенных запятыми или переносами)
    priorities = [p.strip() for p in message.text.replace('\n', ',').split(',') if p.strip()]
    await state.update_data(top3=priorities[:3])  # Берем только первые 3
    
    await message.answer(
        texts.MORNING_ENERGY,
        reply_markup=get_energy_keyboard()
    )
    await state.set_state(Morning.energy)


# Callback обработчик для энергии
@router.callback_query(F.data.startswith("morning:energy:"))
async def process_morning_energy_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора энергии через кнопки."""
    energy = int(callback.data.split(":")[2])
    await state.update_data(energy=energy)
    
    # Завершаем утренний опрос
    await finish_morning_flow(callback, state)
    await callback.answer()


@router.message(Morning.energy)
async def process_morning_energy(message: Message, state: FSMContext):
    """Обрабатывает уровень энергии."""
    try:
        energy = int(message.text)
        if not 1 <= energy <= 10:
            await message.answer("Пожалуйста, введите число от 1 до 10")
            return
    except ValueError:
        await message.answer("Пожалуйста, введите число от 1 до 10")
        return
    
    await state.update_data(energy=energy)
    
    # Завершаем утренний опрос
    await finish_morning_flow(message, state)


async def finish_morning_flow(message_or_callback, state: FSMContext):
    """Завершение утреннего потока."""
    # Получаем все данные
    data = await state.get_data()
    
    # Проверяем наличие обязательных данных
    if 'goal' not in data or 'top3' not in data:
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer("Ошибка: данные не найдены. Начните заново.")
        else:
            await message_or_callback.message.edit_text("Ошибка: данные не найдены. Начните заново.")
        await state.clear()
        return
    
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
    
    # Генерируем план через GPT
    plan = await gpt_service.plan_morning(
        goal=data['goal'],
        top3=data['top3'],
        energy=data.get('energy', 5),
        persona=user.persona,
        memories=memories
    )
    
    # Сохраняем запись в БД
    await db.save_entry(
        tg_id=user_id,
        entry_type="morning",
        data={
            "goal": data['goal'],
            "top3": data['top3'],
            "energy": data.get('energy', 5)
        }
    )
    
    # Добавляем в память
    await memory_service.add_memory(
        tg_id=user_id,
        kind="morning",
        content=f"Утренний план: {data['goal']}, приоритеты: {', '.join(data['top3'])}"
    )
    
    # Сообщение А (финал без кнопок)
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p("Утренний план сохранен! Я всё запомнил.")
            )
        )
    else:
        await message_or_callback.message.edit_text(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p("Утренний план сохранен! Я всё запомнил.")
            )
        )
    
    # Сообщение B (действия с кнопками)
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            ux.compose(
                ux.h1("Что дальше?", "🌅"),
                ux.p("Отличное начало дня! Что планируешь дальше?")
            ),
            reply_markup=kb_post_flow()
        )
    else:
        await message_or_callback.message.answer(
            ux.compose(
                ux.h1("Что дальше?", "🌅"),
                ux.p("Отличное начало дня! Что планируешь дальше?")
            ),
            reply_markup=kb_post_flow()
        )
    
    await state.clear()