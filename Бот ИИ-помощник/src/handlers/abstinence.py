"""Обработчики воздержания."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from ..states import Abstinence
from ..texts import texts
from ..keyboards import get_main_menu, kb_post_flow
from ..storage import db
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("abstinence")
router = Router()


@router.message(F.text == texts.BUTTON_ABSTINENCE)
async def cmd_abstinence(message: Message, state: FSMContext):
    """Обработчик кнопки 'Воздержание'."""
    user_id = message.from_user.id
    
    # Получаем воздержания пользователя
    async with db._connection.execute("""
        SELECT name, start_date, days_count FROM abstinence WHERE tg_id = ? ORDER BY days_count DESC
    """, (user_id,)) as cursor:
        abstinence_list = await cursor.fetchall()
    
    if not abstinence_list:
        await message.answer(
            ux.compose(
                ux.h1("Воздержание", "🚫"),
                ux.p("У тебя пока нет отслеживаемых воздержаний. Давай добавим первое!")
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Добавить воздержание", callback_data="abstinence:add")]
                ]
            )
        )
    else:
        abstinence_text = "\n".join([f"• {item[0]} ({item[2]} дней)" for item in abstinence_list])
        await message.answer(
            ux.compose(
                ux.h1("Твои воздержания", "🚫"),
                ux.p(abstinence_text)
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Добавить", callback_data="abstinence:add")],
                    [InlineKeyboardButton(text="🗑 Удалить", callback_data="abstinence:delete")]
                ]
            )
        )


@router.callback_query(F.data == "abstinence:add")
async def process_abstinence_add_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка добавления воздержания."""
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Добавить воздержание", "➕"),
            ux.p("От чего ты хочешь воздерживаться?")
        )
    )
    await state.set_state(Abstinence.add)
    await callback.answer()


@router.message(Abstinence.add)
async def process_add_abstinence(message: Message, state: FSMContext):
    """Обрабатывает добавление воздержания."""
    user_id = message.from_user.id
    abstinence_name = message.text.strip()
    
    if not abstinence_name:
        await message.answer("Введите название воздержания:")
        return
    
    # Добавляем воздержание в БД
    today = datetime.now().date()
    async with db._connection.execute("""
        INSERT INTO abstinence (tg_id, name, start_date, days_count, created_at)
        VALUES (?, ?, ?, 0, ?)
    """, (user_id, abstinence_name, today, datetime.now())):
        pass
    
    # Финальное сообщение
    await message.answer(
        ux.compose(
            ux.h1("Готово", "✅"),
            ux.p(f"Воздержание '{abstinence_name}' добавлено! Я всё запомнил.")
        )
    )
    await state.clear()


@router.callback_query(F.data == "abstinence:delete")
async def process_abstinence_delete_callback(callback: CallbackQuery, state: FSMContext):
    """Обработка удаления воздержания."""
    user_id = callback.from_user.id
    
    # Получаем воздержания пользователя
    async with db._connection.execute("""
        SELECT name, days_count FROM abstinence WHERE tg_id = ? ORDER BY days_count DESC
    """, (user_id,)) as cursor:
        abstinence_list = await cursor.fetchall()
    
    if not abstinence_list:
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Нет воздержаний", "🚫"),
                ux.p("У тебя пока нет воздержаний для удаления.")
            )
        )
        await callback.answer()
        return
    
    # Создаем кнопки для выбора воздержания
    buttons = []
    for i, (name, days) in enumerate(abstinence_list):
        buttons.append([InlineKeyboardButton(
            text=f"{name} ({days} дней)", 
            callback_data=f"abstinence:delete:{i}"
        )])
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Удалить воздержание", "🗑"),
            ux.p("Какое воздержание хочешь удалить?")
        ),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("abstinence:delete:"))
async def process_abstinence_delete_select(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора воздержания для удаления."""
    user_id = callback.from_user.id
    abstinence_idx = int(callback.data.split(":")[2])
    
    # Получаем воздержания пользователя
    async with db._connection.execute("""
        SELECT name, days_count FROM abstinence WHERE tg_id = ? ORDER BY days_count DESC
    """, (user_id,)) as cursor:
        abstinence_list = await cursor.fetchall()
    
    if abstinence_idx < len(abstinence_list):
        abstinence_name = abstinence_list[abstinence_idx][0]
        
        # Удаляем воздержание из БД
        async with db._connection.execute("""
            DELETE FROM abstinence WHERE tg_id = ? AND name = ?
        """, (user_id, abstinence_name)):
            pass
        
        # Финальное сообщение
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Готово", "✅"),
                ux.p(f"Воздержание '{abstinence_name}' удалено.")
            )
        )
    
    await callback.answer()
