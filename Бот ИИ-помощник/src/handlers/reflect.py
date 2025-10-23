"""Обработчики диалога с цифровым Я."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import Reflect
from ..texts import texts
from ..keyboards import kb_reflect_topics, kb_reflect_actions, kb_post_flow, get_main_menu
from ..storage import db
from ..services.gpt import gpt_service
from ..services.memories import memory_service
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("reflect")
router = Router()


@router.message(F.text.in_({"🧩 Цифровое Я", "/reflect"}))
async def reflect_start(msg: Message, state: FSMContext):
    """Начало диалога с цифровым Я."""
    # Убираем проверку доступа - функция доступна всем
    
    await state.set_state(Reflect.topic)
    await msg.answer(
        ux.compose(
            ux.h1("Цифровое Я", "🧩"),
            ux.p("О чём поговорим?")
        ),
        reply_markup=kb_reflect_topics()
    )


@router.callback_query(F.data.startswith("reflect:topic:"))
async def process_topic_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора темы."""
    topic_idx = callback.data.split(":")[2]
    
    if topic_idx == "custom":
        await state.set_state(Reflect.prompt)
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Цифровое Я", "🧩"),
                ux.p("Напиши свой вопрос:")
            )
        )
        await callback.answer()
        return
    
    # Выбираем из пресетов
    topic = texts.REFLECT_TOPICS[int(topic_idx)]
    await state.update_data(topic=topic)
    await state.set_state(Reflect.prompt)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Цифровое Я", "🧩"),
            ux.p(f"Тема: {topic}"),
            ux.p("Задай свой вопрос:")
        )
    )
    await callback.answer()


@router.message(Reflect.prompt)
async def process_reflect_prompt(msg: Message, state: FSMContext):
    """Обработка вопроса пользователя."""
    question = msg.text.strip()
    data = await state.get_data()
    topic = data.get('topic', 'Общий вопрос')
    
    # Получаем пользователя и его персону
    user = await db.get_user(msg.from_user.id)
    if not user:
        await msg.answer(texts.ERROR_NOT_FOUND)
        return
    
    # Получаем контекст из памяти
    memories = await memory_service.get_recent_memories(msg.from_user.id, 5)
    
    # Генерируем ответ через GPT
    response = await gpt_service.reflect_dialog(
        user_prompt=question,
        profile=user.profile_data or {},
        persona=user.persona or "Дружелюбный помощник",
        memories=memories,
        mood_snapshot={"energy": 5, "mood": 5}  # Значения по умолчанию
    )
    
    # Показываем ответ
    await msg.answer(
        ux.compose(
            ux.h1("Ответ цифрового Я", "🤖"),
            ux.block("Размышление", response.split("\n"), "💭")
        ),
        reply_markup=kb_reflect_actions()
    )


@router.callback_query(F.data == "reflect:clarify")
async def process_clarify(callback: CallbackQuery, state: FSMContext):
    """Уточнение вопроса."""
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Цифровое Я", "🧩"),
            ux.p("Задай уточняющий вопрос:")
        )
    )
    await callback.answer()


@router.callback_query(F.data == "reflect:save")
async def process_save_insight(callback: CallbackQuery, state: FSMContext):
    """Сохранение инсайта."""
    # Получаем последний ответ из контекста
    # В реальном приложении нужно сохранить ответ в состояние
    insight = "Важный инсайт из диалога"
    
    # Сохраняем в память
    await memory_service.add_memory(
        callback.from_user.id,
        "reflect",
        insight
    )
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Инсайт сохранён", "📌"),
            ux.p("Я запомнил этот важный момент для будущих разговоров.")
        ),
        reply_markup=kb_post_flow()
    )
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "nav:menu")
async def process_back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в меню."""
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Цифровое Я", "🧩"),
            ux.p("До свидания! Возвращайся, когда захочешь поговорить.")
        ),
        reply_markup=None
    )
    await callback.answer()
    await state.clear()


# Удален обработчик команд /выход и /меню - они больше не нужны