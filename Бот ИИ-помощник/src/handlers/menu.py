"""Обработчики главного меню."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from ..states import Morning, Evening, Focus, Habits, Mood, Reflect
from ..texts import texts
from ..keyboards import get_main_menu, kb_morning_goal, kb_evening_done
from ..services import ux
from ..storage import db
from ..logger import get_logger

logger = get_logger("menu")
router = Router()


@router.message(F.text == texts.BUTTON_DAY)
async def cmd_day(message: Message, state: FSMContext):
    """Обработчик кнопки 'Мой день'."""
    user_id = message.from_user.id
    logger.info(f"Day button pressed by user {user_id}")
    
    try:
        # Проверяем время и предлагаем соответствующий опрос
        from datetime import datetime
        from ..services.timeutils import time_utils
    
        # Получаем пользователя для определения часового пояса
        from ..storage import db
        user = await db.get_user(user_id)
        if not user:
            await message.answer("Пользователь не найден. Начните с /start")
            return
        
        # Определяем локальное время
        local_time = time_utils.now_local(user.tz)
        hour = local_time.hour
        logger.info(f"User {user_id} local time: {local_time}, hour: {hour}")
        
        # Логика выбора опроса
        if 0 <= hour < 12:  # Утро
            await message.answer(
                ux.compose(
                    ux.h1("Мой день", "📅"),
                    ux.p("Доброе утро! Начнем с планирования дня.")
                ),
                reply_markup=kb_morning_goal()
            )
            await state.set_state(Morning.goal)
        elif 17 <= hour < 24:  # Вечер
            await message.answer(
                ux.compose(
                    ux.h1("Мой день", "📅"),
                    ux.p("Добрый вечер! Подведем итоги дня.")
                ),
                reply_markup=kb_evening_done()
            )
            await state.set_state(Evening.done)
        else:  # День - показываем выбор
            await message.answer(
                ux.compose(
                    ux.h1("Мой день", "📅"),
                    ux.p("Что хочешь сделать?")
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="☀️ Утренний опрос", callback_data="day:morning")],
                        [InlineKeyboardButton(text="🌙 Вечерний опрос", callback_data="day:evening")]
                    ]
                )
            )
    except Exception as e:
        logger.error(f"Error in cmd_day: {e}")
        await message.answer("Ошибка при обработке запроса. Попробуйте позже.")


@router.callback_query(F.data == "day:morning")
async def process_day_morning(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора утреннего опроса."""
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Мой день", "📅"),
            ux.p("Доброе утро! Начнем с планирования дня.")
        ),
        reply_markup=kb_morning_goal()
    )
    await state.set_state(Morning.goal)
    await callback.answer()


@router.callback_query(F.data == "day:evening")
async def process_day_evening(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора вечернего опроса."""
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Мой день", "📅"),
            ux.p("Добрый вечер! Подведем итоги дня.")
        ),
        reply_markup=kb_evening_done()
    )
    await state.set_state(Evening.done)
    await callback.answer()


@router.message(F.text == texts.BUTTON_FOCUS)
async def cmd_focus(message: Message, state: FSMContext):
    """Обработчик кнопки 'Фокус-сессия'."""
    from ..keyboards import get_focus_duration_keyboard
    await message.answer(
        texts.FOCUS_SELECT,
        reply_markup=get_focus_duration_keyboard()
    )
    await state.set_state(Focus.selecting)


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


# Обработчик настроения перенесен в src/handlers/mood.py


@router.message(F.text == texts.BUTTON_REFLECT)
async def cmd_reflect(message: Message, state: FSMContext):
    """Обработчик кнопки 'Цифровое Я'."""
    # Проверяем подписку и пробный период
    from ..storage import db
    from datetime import datetime
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer(texts.ERROR_NOT_FOUND)
        return
    
    # Проверяем пробный период
    if user.trial_until and user.trial_until > datetime.now():
        # Пробный период активен - разрешаем доступ
        pass
    elif user.plan_tier in ["pro", "mentor", "ultimate"] and user.subscription_until and user.subscription_until > datetime.now():
        # Активная подписка
        pass
    else:
        await message.answer(texts.PAYWALL)
        return
    
    await message.answer(
        texts.REFLECT_PROMPT,
        reply_markup=None
    )
    await state.set_state(Reflect.prompt)


@router.message(F.text == texts.BUTTON_WEEKLY)
async def cmd_weekly(message: Message, state: FSMContext):
    """Обработчик кнопки 'Отчёт недели'."""
    from ..services.reports import report_service
    from ..storage import db
    
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer(texts.ERROR_NOT_FOUND)
        return
    
    # Генерируем отчет
    report = await report_service.generate_weekly_report(user_id, user.persona)
    
    await message.answer(
        texts.WEEKLY_REPORT.format(report=report),
        reply_markup=get_main_menu()
    )


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


@router.message(F.text == texts.BUTTON_SETTINGS)
async def cmd_settings(message: Message, state: FSMContext):
    """Обработчик кнопки 'Настройки'."""
    from ..storage import db
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer(texts.ERROR_NOT_FOUND)
        return
    
    settings_text = texts.SETTINGS_MENU.format(
        tz=user.tz,
        morning_hour=user.morning_hour,
        evening_hour=user.evening_hour,
        language=user.language,
        persona=user.persona
    )
    
    await message.answer(settings_text, reply_markup=get_main_menu())


@router.message(F.text == texts.BUTTON_BILLING)
async def cmd_billing(message: Message, state: FSMContext):
    """Обработчик кнопки 'Подписка' - демо-режим."""
    from ..services import ux
    from ..keyboards import kb_subscriptions
    
    title = ux.h1(texts.SUBSCRIBE_TITLE, "💳")
    intro = ux.p(texts.SUBSCRIBE_DESC)
    plans = []
    for key, meta in texts.SUBSCRIBE_PLANS.items():
        plans.append(f"{meta['name']} — {ux.escape(meta['desc'])}")
    body = ux.block("Доступные тарифы", plans, "📦")
    await message.answer(ux.compose(title, intro, body), reply_markup=kb_subscriptions())
