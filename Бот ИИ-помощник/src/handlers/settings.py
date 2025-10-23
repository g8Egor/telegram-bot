"""Обработчики настроек."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import Settings
from ..texts import texts
from ..keyboards import (
    kb_settings_tz, kb_settings_time, kb_settings_language, kb_settings_persona,
    kb_settings_clear, kb_post_flow, get_main_menu
)
from ..storage import db
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("settings")
router = Router()


@router.message(F.text.in_({"⚙️ Настройки", "/settings"}))
async def settings_start(msg: Message, state: FSMContext):
    """Начало настроек."""
    user = await db.get_user(msg.from_user.id)
    if not user:
        await msg.answer(texts.ERROR_NOT_FOUND)
        return
    
    await msg.answer(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(texts.SETTINGS_MENU.format(
                tz=user.tz,
                morning_hour=user.morning_hour,
                evening_hour=user.evening_hour,
                language=user.language,
                persona=user.persona
            ))
        ),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🌍 Часовой пояс", callback_data="settings:tz")],
                [InlineKeyboardButton(text="⏰ Время утра/вечера", callback_data="settings:time")],
                [InlineKeyboardButton(text="🗣️ Язык", callback_data="settings:lang")],
                [InlineKeyboardButton(text="👤 Персона", callback_data="settings:persona")],
                [InlineKeyboardButton(text="🧹 Очистить память", callback_data="settings:clear")],
                [InlineKeyboardButton(text="↩️ В меню", callback_data="nav:menu")]
            ]
        )
    )


@router.callback_query(F.data == "settings:tz")
async def process_tz_setting(callback: CallbackQuery, state: FSMContext):
    """Настройка часового пояса."""
    await state.set_state(Settings.tz)
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(texts.SETTINGS_TZ_TITLE)
        ),
        reply_markup=kb_settings_tz()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("settings:tz:"))
async def process_tz_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора часового пояса."""
    tz = callback.data.split(":")[2]
    
    if tz == "custom":
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Настройки", "⚙️"),
                ux.p("Введи часовой пояс (например: Europe/Moscow):")
            )
        )
        await callback.answer()
        return
    
    # Обновляем часовой пояс
    await db.update_user_tz(callback.from_user.id, tz)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(f"Часовой пояс установлен: {tz}")
        ),
        reply_markup=kb_post_flow()
    )
    await callback.answer()
    await state.clear()


@router.message(Settings.tz)
async def process_tz_custom(msg: Message, state: FSMContext):
    """Обработка кастомного часового пояса."""
    tz = msg.text.strip()
    
    # Обновляем часовой пояс
    await db.update_user_tz(msg.from_user.id, tz)
    
    await msg.answer(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(f"Часовой пояс установлен: {tz}")
        ),
        reply_markup=kb_post_flow()
    )
    await state.clear()


@router.callback_query(F.data == "settings:time")
async def process_time_setting(callback: CallbackQuery, state: FSMContext):
    """Настройка времени утра/вечера."""
    await state.set_state(Settings.time)
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(texts.SETTINGS_TIME_TITLE)
        ),
        reply_markup=kb_settings_time()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("settings:time:"))
async def process_time_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора времени."""
    time_type = callback.data.split(":")[2]
    
    if time_type == "morning":
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Настройки", "⚙️"),
                ux.p("Выбери время утреннего опроса:")
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="07:00", callback_data="time:morning:7")],
                    [InlineKeyboardButton(text="08:00", callback_data="time:morning:8")],
                    [InlineKeyboardButton(text="09:00", callback_data="time:morning:9")],
                    [InlineKeyboardButton(text="10:00", callback_data="time:morning:10")]
                ]
            )
        )
    elif time_type == "evening":
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Настройки", "⚙️"),
                ux.p("Выбери время вечернего опроса:")
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="18:00", callback_data="time:evening:18")],
                    [InlineKeyboardButton(text="19:00", callback_data="time:evening:19")],
                    [InlineKeyboardButton(text="20:00", callback_data="time:evening:20")],
                    [InlineKeyboardButton(text="21:00", callback_data="time:evening:21")]
                ]
            )
        )
    
    await callback.answer()


@router.callback_query(F.data.startswith("time:"))
async def process_time_update(callback: CallbackQuery, state: FSMContext):
    """Обновление времени."""
    time_type, hour = callback.data.split(":")[1], int(callback.data.split(":")[2])
    
    if time_type == "morning":
        await db.update_user_morning_hour(callback.from_user.id, hour)
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Настройки", "⚙️"),
                ux.p(f"Утренний опрос установлен на {hour}:00")
            ),
            reply_markup=kb_post_flow()
        )
    elif time_type == "evening":
        await db.update_user_evening_hour(callback.from_user.id, hour)
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Настройки", "⚙️"),
                ux.p(f"Вечерний опрос установлен на {hour}:00")
            ),
            reply_markup=kb_post_flow()
        )
    
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "settings:lang")
async def process_language_setting(callback: CallbackQuery, state: FSMContext):
    """Настройка языка."""
    await state.set_state(Settings.language)
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(texts.SETTINGS_LANGUAGE_TITLE)
        ),
        reply_markup=kb_settings_language()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("settings:lang:"))
async def process_language_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора языка."""
    lang = callback.data.split(":")[2]
    
    # Обновляем язык
    await db.update_user_language(callback.from_user.id, lang)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(f"Язык установлен: {lang}")
        ),
        reply_markup=kb_post_flow()
    )
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "settings:persona")
async def process_persona_setting(callback: CallbackQuery, state: FSMContext):
    """Настройка персоны."""
    await state.set_state(Settings.persona)
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(texts.SETTINGS_PERSONA_TITLE)
        ),
        reply_markup=kb_settings_persona()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("settings:persona:"))
async def process_persona_selection(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора персоны."""
    persona = callback.data.split(":")[2]
    
    # Обновляем персону
    await db.update_user_persona(callback.from_user.id, persona)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(f"Персона установлена: {persona}")
        ),
        reply_markup=kb_post_flow()
    )
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "settings:clear")
async def process_clear_setting(callback: CallbackQuery, state: FSMContext):
    """Настройка очистки памяти."""
    await state.set_state(Settings.clear)
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Настройки", "⚙️"),
            ux.p(texts.SETTINGS_CLEAR_TITLE),
            ux.p(texts.SETTINGS_CLEAR_CONFIRM)
        ),
        reply_markup=kb_settings_clear()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("settings:clear:"))
async def process_clear_confirmation(callback: CallbackQuery, state: FSMContext):
    """Обработка подтверждения очистки."""
    action = callback.data.split(":")[2]
    
    if action == "yes":
        # Очищаем память за последние 7 дней
        await db.clear_user_memories(callback.from_user.id, days=7)
        
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Настройки", "⚙️"),
                ux.p("Память очищена за последние 7 дней")
            ),
            reply_markup=kb_post_flow()
        )
    else:
        await callback.message.edit_text(
            ux.compose(
                ux.h1("Настройки", "⚙️"),
                ux.p("Очистка отменена")
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
            ux.h1("Настройки", "⚙️"),
            ux.p("Настройки сохранены!")
        ),
        reply_markup=None
    )
    await callback.answer()
    await state.clear()