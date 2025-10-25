"""Клавиатуры бота."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .texts import texts


def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BUTTON_DAY), KeyboardButton(text=texts.BUTTON_FOCUS)],
            [KeyboardButton(text=texts.BUTTON_HABITS), KeyboardButton(text=texts.BUTTON_MOOD)],
            [KeyboardButton(text=texts.BUTTON_REFLECT), KeyboardButton(text=texts.BUTTON_WEEKLY)],
            [KeyboardButton(text=texts.BUTTON_ABSTINENCE), KeyboardButton(text=texts.BUTTON_SETTINGS)],
            [KeyboardButton(text=texts.BUTTON_BILLING)]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


def get_yes_no_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура Да/Нет."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BUTTON_YES), KeyboardButton(text=texts.BUTTON_NO)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой Отмена."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BUTTON_CANCEL)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_focus_duration_keyboard(is_pro: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура выбора продолжительности фокус-сессии."""
    buttons = [
        [InlineKeyboardButton(text=texts.BUTTON_25_MIN, callback_data="focus:start:25")]
    ]
    
    if is_pro:
        buttons.append([InlineKeyboardButton(text=texts.BUTTON_45_MIN, callback_data="focus:start:45")])
    
    buttons.append([InlineKeyboardButton(text=texts.BUTTON_CANCEL, callback_data="focus:cancel")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_focus_control_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура управления фокус-сессией."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.BUTTON_PAUSE, callback_data="focus_pause")],
            [InlineKeyboardButton(text=texts.BUTTON_STOP, callback_data="focus_stop")],
            [InlineKeyboardButton(text=texts.BUTTON_DONE, callback_data="focus_done")]
        ]
    )
    return keyboard


def get_focus_paused_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для приостановленной фокус-сессии."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="▶️ Продолжить", callback_data="focus_resume")],
            [InlineKeyboardButton(text=texts.BUTTON_STOP, callback_data="focus_stop")],
            [InlineKeyboardButton(text=texts.BUTTON_DONE, callback_data="focus_done")]
        ]
    )
    return keyboard


def get_energy_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора уровня энергии для настроения."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_1, callback_data="mood_energy_1"),
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_2, callback_data="mood_energy_2"),
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_3, callback_data="mood_energy_3"),
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_4, callback_data="mood_energy_4"),
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_5, callback_data="mood_energy_5")
            ],
            [
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_6, callback_data="mood_energy_6"),
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_7, callback_data="mood_energy_7"),
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_8, callback_data="mood_energy_8"),
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_9, callback_data="mood_energy_9"),
                InlineKeyboardButton(text=texts.BUTTON_ENERGY_10, callback_data="mood_energy_10")
            ]
        ]
    )
    return keyboard


def get_mood_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора настроения."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts.BUTTON_MOOD_1, callback_data="mood_1"),
                InlineKeyboardButton(text=texts.BUTTON_MOOD_2, callback_data="mood_2"),
                InlineKeyboardButton(text=texts.BUTTON_MOOD_3, callback_data="mood_3"),
                InlineKeyboardButton(text=texts.BUTTON_MOOD_4, callback_data="mood_4"),
                InlineKeyboardButton(text=texts.BUTTON_MOOD_5, callback_data="mood_5")
            ],
            [
                InlineKeyboardButton(text=texts.BUTTON_MOOD_6, callback_data="mood_6"),
                InlineKeyboardButton(text=texts.BUTTON_MOOD_7, callback_data="mood_7"),
                InlineKeyboardButton(text=texts.BUTTON_MOOD_8, callback_data="mood_8"),
                InlineKeyboardButton(text=texts.BUTTON_MOOD_9, callback_data="mood_9"),
                InlineKeyboardButton(text=texts.BUTTON_MOOD_10, callback_data="mood_10")
            ]
        ]
    )
    return keyboard


def get_habits_keyboard(habits: list) -> InlineKeyboardMarkup:
    """Клавиатура управления привычками."""
    keyboard_buttons = []
    
    # Кнопки для каждой привычки
    for i, habit in enumerate(habits):
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"✅ {habit['name']} ({habit['streak']})",
                callback_data=f"habit_tick_{i}"
            )
        ])
    
    # Кнопки управления
    keyboard_buttons.append([
        InlineKeyboardButton(text=texts.BUTTON_ADD_HABIT, callback_data="habit_add"),
        InlineKeyboardButton(text=texts.BUTTON_REMOVE_HABIT, callback_data="habit_remove")
    ])
    
    keyboard_buttons.append([
        InlineKeyboardButton(text=texts.BUTTON_BACK, callback_data="back_to_menu")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard


def get_billing_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура тарифов."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.BUTTON_FREE, callback_data="plan_free")],
            [InlineKeyboardButton(text=texts.BUTTON_PRO, callback_data="plan_pro")],
            [InlineKeyboardButton(text=texts.BUTTON_MENTOR, callback_data="plan_mentor")],
            [InlineKeyboardButton(text=texts.BUTTON_ULTIMATE, callback_data="plan_ultimate")],
            [InlineKeyboardButton(text=texts.BUTTON_CHECK, callback_data="check_payment")],
            [InlineKeyboardButton(text=texts.BUTTON_BACK, callback_data="back_to_menu")]
        ]
    )
    return keyboard


def get_period_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора периода подписки."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.BUTTON_MONTHLY, callback_data="period_monthly")],
            [InlineKeyboardButton(text=texts.BUTTON_YEARLY, callback_data="period_yearly")],
            [InlineKeyboardButton(text=texts.BUTTON_BACK, callback_data="back_to_menu")]
        ]
    )
    return keyboard


def get_persona_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора персоны."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.BUTTON_MENTOR, callback_data="persona_mentor")],
            [InlineKeyboardButton(text=texts.BUTTON_COACH, callback_data="persona_coach")],
            [InlineKeyboardButton(text=texts.BUTTON_FRIEND, callback_data="persona_friend")],
            [InlineKeyboardButton(text=texts.BUTTON_ANALYST, callback_data="persona_analyst")],
            [InlineKeyboardButton(text=texts.BUTTON_BACK, callback_data="back_to_settings")]
        ]
    )
    return keyboard


def kb_subscriptions() -> InlineKeyboardMarkup:
    """Клавиатура для выбора подписки."""
    rows = [
        [
            InlineKeyboardButton(text="⚡ Pro — 100 ₽/мес", callback_data="plan:pro:month"),
            InlineKeyboardButton(text="⚡ Pro — 1000 ₽/год",   callback_data="plan:pro:year"),
        ],
        [
            InlineKeyboardButton(text="🔮 Mentor — 200 ₽/мес", callback_data="plan:mentor:month"),
            InlineKeyboardButton(text="🔮 Mentor — 2000 ₽/год",   callback_data="plan:mentor:year"),
        ],
        [
            InlineKeyboardButton(text="🧬 Ultimate — 300 ₽/мес", callback_data="plan:ult:month"),
            InlineKeyboardButton(text="🧬 Ultimate — 3000 ₽/год",   callback_data="plan:ult:year"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура настроек."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌍 Часовой пояс", callback_data="setting_tz")],
            [InlineKeyboardButton(text="🌅 Утренний час", callback_data="setting_morning")],
            [InlineKeyboardButton(text="🌙 Вечерний час", callback_data="setting_evening")],
            [InlineKeyboardButton(text="🗣️ Язык", callback_data="setting_language")],
            [InlineKeyboardButton(text="👤 Персона", callback_data="setting_persona")],
            [InlineKeyboardButton(text=texts.BUTTON_BACK, callback_data="back_to_menu")]
        ]
    )
    return keyboard


def kb_post_flow() -> InlineKeyboardMarkup:
    """Универсальная клавиатура после завершения потока."""
    rows = [
        [InlineKeyboardButton(text="📊 Статистика дня", callback_data="nav:stats")],
        [InlineKeyboardButton(text="🎯 Фокус-сессия", callback_data="focus:open")],
        [InlineKeyboardButton(text="↩️ В меню", callback_data="nav:menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def kb_cancel_reply() -> ReplyKeyboardMarkup:
    """Клавиатура отмены для FSM."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_timezone_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора часового пояса."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Москва", callback_data="tz_Europe/Moscow")],
            [InlineKeyboardButton(text="🇪🇺 Амстердам", callback_data="tz_Europe/Amsterdam")],
            [InlineKeyboardButton(text="🇺🇸 Нью-Йорк", callback_data="tz_America/New_York")],
            [InlineKeyboardButton(text="🇬🇧 Лондон", callback_data="tz_Europe/London")],
            [InlineKeyboardButton(text="🇯🇵 Токио", callback_data="tz_Asia/Tokyo")],
            [InlineKeyboardButton(text=texts.BUTTON_BACK, callback_data="back_to_settings")]
        ]
    )
    return keyboard


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
            [InlineKeyboardButton(text=texts.BUTTON_BACK, callback_data="back_to_settings")]
        ]
    )
    return keyboard


def get_hour_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора часа."""
    keyboard_buttons = []
    
    # Создаем кнопки для каждого часа
    for hour in range(24):
        if hour % 4 == 0:  # Группируем по 4 кнопки в ряд
            row = []
        row.append(InlineKeyboardButton(
            text=f"{hour:02d}:00",
            callback_data=f"hour_{hour}"
        ))
        if hour % 4 == 3 or hour == 23:
            keyboard_buttons.append(row)
    
    keyboard_buttons.append([
        InlineKeyboardButton(text=texts.BUTTON_BACK, callback_data="back_to_settings")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard


# Профиль 10Q - кнопочные клавиатуры
def kb_profile_q1() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 1 (время пробуждения)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A1):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q1:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q2() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 2 (мотивация)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A2):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q2:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q3() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 3 (сильные стороны)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A3):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q3:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q4() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 4 (слабость)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A4):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q4:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q5() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 5 (длительность фокуса)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A5):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q5:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q6() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 6 (стресс)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A6):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q6:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q7() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 7 (стиль общения)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A7):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q7:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q8() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 8 (идеальное утро)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A8):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q8:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q9() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 9 (идеальный вечер)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A9):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q9:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_q10() -> InlineKeyboardMarkup:
    """Клавиатура для вопроса 10 (цель на неделю)."""
    buttons = []
    for i, option in enumerate(texts.PROFILE_A10):
        buttons.append([InlineKeyboardButton(text=option, callback_data=f"profile:q10:{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_profile_persona() -> InlineKeyboardMarkup:
    """Клавиатура выбора персоны после профиля."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.SETTINGS_PERSONA_MENTOR, callback_data="profile:persona:mentor")],
            [InlineKeyboardButton(text=texts.SETTINGS_PERSONA_COACH, callback_data="profile:persona:coach")],
            [InlineKeyboardButton(text=texts.SETTINGS_PERSONA_FRIEND, callback_data="profile:persona:friend")],
            [InlineKeyboardButton(text=texts.SETTINGS_PERSONA_ANALYST, callback_data="profile:persona:analyst")]
        ]
    )


# Утро - кнопочные клавиатуры
def kb_morning_goal() -> InlineKeyboardMarkup:
    """Клавиатура выбора цели на день."""
    buttons = []
    for i, goal in enumerate(texts.MORNING_GOAL_PRESETS):
        buttons.append([InlineKeyboardButton(text=goal, callback_data=f"morning:goal:{i}")])
    buttons.append([InlineKeyboardButton(text=texts.MORNING_GOAL_CUSTOM, callback_data="morning:goal:custom")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_morning_tasks() -> InlineKeyboardMarkup:
    """Клавиатура выбора задач."""
    buttons = []
    for i, task in enumerate(texts.MORNING_TASKS_PRESETS):
        buttons.append([InlineKeyboardButton(text=task, callback_data=f"morning:task:{i}")])
    buttons.append([InlineKeyboardButton(text=texts.MORNING_TASKS_ADD, callback_data="morning:task:add")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_morning_energy() -> InlineKeyboardMarkup:
    """Клавиатура энергии (1-10)."""
    buttons = []
    for i in range(1, 11):
        buttons.append(InlineKeyboardButton(text=str(i), callback_data=f"morning:energy:{i}"))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


# Вечер - кнопочные клавиатуры
def kb_evening_done() -> InlineKeyboardMarkup:
    """Клавиатура что удалось."""
    buttons = []
    for i, item in enumerate(texts.EVENING_DONE_PRESETS):
        buttons.append([InlineKeyboardButton(text=item, callback_data=f"evening:done:{i}")])
    buttons.append([InlineKeyboardButton(text=texts.EVENING_DONE_CUSTOM, callback_data="evening:done:custom")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_evening_not_done() -> InlineKeyboardMarkup:
    """Клавиатура что не получилось."""
    buttons = []
    for i, item in enumerate(texts.EVENING_NOT_DONE_PRESETS):
        buttons.append([InlineKeyboardButton(text=item, callback_data=f"evening:not_done:{i}")])
    buttons.append([InlineKeyboardButton(text=texts.EVENING_NOT_DONE_CUSTOM, callback_data="evening:not_done:custom")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_evening_learning() -> InlineKeyboardMarkup:
    """Клавиатура чему научился."""
    buttons = []
    for i, item in enumerate(texts.EVENING_LEARNING_PRESETS):
        buttons.append([InlineKeyboardButton(text=item, callback_data=f"evening:learning:{i}")])
    buttons.append([InlineKeyboardButton(text=texts.EVENING_LEARNING_CUSTOM, callback_data="evening:learning:custom")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Настроение - только кнопки
def kb_mood_energy() -> InlineKeyboardMarkup:
    """Клавиатура энергии для настроения."""
    buttons = []
    # Первый ряд: 1-5
    row1 = [InlineKeyboardButton(text=str(i), callback_data=f"mood:energy:{i}") for i in range(1, 6)]
    buttons.append(row1)
    # Второй ряд: 6-10
    row2 = [InlineKeyboardButton(text=str(i), callback_data=f"mood:energy:{i}") for i in range(6, 11)]
    buttons.append(row2)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_mood_feel() -> InlineKeyboardMarkup:
    """Клавиатура настроения."""
    buttons = []
    # Первый ряд: 1-5
    row1 = [InlineKeyboardButton(text=str(i), callback_data=f"mood:feel:{i}") for i in range(1, 6)]
    buttons.append(row1)
    # Второй ряд: 6-10
    row2 = [InlineKeyboardButton(text=str(i), callback_data=f"mood:feel:{i}") for i in range(6, 11)]
    buttons.append(row2)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_mood_note() -> InlineKeyboardMarkup:
    """Клавиатура заметки настроения."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.MOOD_NOTE_ADD, callback_data="mood:note:add")],
            [InlineKeyboardButton(text=texts.MOOD_NOTE_SKIP, callback_data="mood:note:skip")]
        ]
    )


# Фокус-сессия
def kb_focus_duration() -> InlineKeyboardMarkup:
    """Клавиатура выбора длительности фокуса."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.FOCUS_25_MIN, callback_data="focus:start:25")],
            [InlineKeyboardButton(text=texts.FOCUS_45_MIN, callback_data="focus:start:45")]
        ]
    )


def kb_focus_controls() -> InlineKeyboardMarkup:
    """Клавиатура управления фокус-сессией."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏸ Пауза", callback_data="focus:pause"),
                InlineKeyboardButton(text="✅ Готово", callback_data="focus:done")
            ]
        ]
    )


def kb_focus_reflection() -> InlineKeyboardMarkup:
    """Клавиатура рефлексии фокуса."""
    buttons = []
    for i, item in enumerate(texts.FOCUS_REFLECTION_PRESETS):
        buttons.append([InlineKeyboardButton(text=item, callback_data=f"focus:reflection:{i}")])
    buttons.append([InlineKeyboardButton(text=texts.FOCUS_REFLECTION_CUSTOM, callback_data="focus:reflection:custom")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Цифровое Я
def kb_reflect_topics() -> InlineKeyboardMarkup:
    """Клавиатура тем для рефлексии."""
    buttons = []
    for i, topic in enumerate(texts.REFLECT_TOPICS):
        buttons.append([InlineKeyboardButton(text=topic, callback_data=f"reflect:topic:{i}")])
    buttons.append([InlineKeyboardButton(text=texts.REFLECT_TOPICS_CUSTOM, callback_data="reflect:topic:custom")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_reflect_actions() -> InlineKeyboardMarkup:
    """Клавиатура действий после ответа."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts.REFLECT_ACTIONS[0], callback_data="reflect:clarify"),
                InlineKeyboardButton(text=texts.REFLECT_ACTIONS[1], callback_data="reflect:save")
            ],
            [InlineKeyboardButton(text=texts.REFLECT_ACTIONS[2], callback_data="nav:menu")]
        ]
    )


# Настройки
def kb_settings_tz() -> InlineKeyboardMarkup:
    """Клавиатура часовых поясов."""
    buttons = []
    for tz in texts.SETTINGS_TZ_POPULAR:
        buttons.append([InlineKeyboardButton(text=tz, callback_data=f"settings:tz:{tz}")])
    buttons.append([InlineKeyboardButton(text=texts.SETTINGS_TZ_CUSTOM, callback_data="settings:tz:custom")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_settings_time() -> InlineKeyboardMarkup:
    """Клавиатура настройки времени."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts.SETTINGS_TIME_MORNING, callback_data="settings:time:morning"),
                InlineKeyboardButton(text=texts.SETTINGS_TIME_EVENING, callback_data="settings:time:evening")
            ]
        ]
    )


def kb_settings_language() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.SETTINGS_LANGUAGE_RU, callback_data="settings:lang:ru")],
            [InlineKeyboardButton(text=texts.SETTINGS_LANGUAGE_EN, callback_data="settings:lang:en")]
        ]
    )


def kb_settings_persona() -> InlineKeyboardMarkup:
    """Клавиатура выбора персоны."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.SETTINGS_PERSONA_MENTOR, callback_data="settings:persona:mentor")],
            [InlineKeyboardButton(text=texts.SETTINGS_PERSONA_COACH, callback_data="settings:persona:coach")],
            [InlineKeyboardButton(text=texts.SETTINGS_PERSONA_FRIEND, callback_data="settings:persona:friend")],
            [InlineKeyboardButton(text=texts.SETTINGS_PERSONA_ANALYST, callback_data="settings:persona:analyst")]
        ]
    )


def kb_settings_clear() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения очистки."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.SETTINGS_CLEAR_YES, callback_data="settings:clear:yes")],
            [InlineKeyboardButton(text=texts.SETTINGS_CLEAR_NO, callback_data="settings:clear:no")]
        ]
    )


# Экспорт
def kb_export() -> InlineKeyboardMarkup:
    """Клавиатура экспорта."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=texts.EXPORT_TODAY, callback_data="export:today")],
            [InlineKeyboardButton(text=texts.EXPORT_WEEK, callback_data="export:week")]
        ]
    )


# Утренние клавиатуры
def kb_morning_goal() -> InlineKeyboardMarkup:
    """Клавиатура выбора цели на день."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Работа над проектом", callback_data="morning:goal:0")],
            [InlineKeyboardButton(text="Изучение нового", callback_data="morning:goal:1")],
            [InlineKeyboardButton(text="Физическая активность", callback_data="morning:goal:2")],
            [InlineKeyboardButton(text="Встречи и общение", callback_data="morning:goal:3")],
            [InlineKeyboardButton(text="Отдых и восстановление", callback_data="morning:goal:4")],
            [InlineKeyboardButton(text="✍️ Свой вариант", callback_data="morning:goal:custom")]
        ]
    )


def kb_morning_tasks() -> InlineKeyboardMarkup:
    """Клавиатура выбора задач."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Планирование", callback_data="morning:task:0")],
            [InlineKeyboardButton(text="Кодинг", callback_data="morning:task:1")],
            [InlineKeyboardButton(text="Изучение", callback_data="morning:task:2")],
            [InlineKeyboardButton(text="Встречи", callback_data="morning:task:3")],
            [InlineKeyboardButton(text="Спорт", callback_data="morning:task:4")],
            [InlineKeyboardButton(text="✍️ Добавить свои", callback_data="morning:task:add")]
        ]
    )


def kb_morning_energy() -> InlineKeyboardMarkup:
    """Клавиатура энергии для утра."""
    buttons = []
    # Первый ряд: 1-5
    row1 = [InlineKeyboardButton(text=str(i), callback_data=f"morning:energy:{i}") for i in range(1, 6)]
    buttons.append(row1)
    # Второй ряд: 6-10
    row2 = [InlineKeyboardButton(text=str(i), callback_data=f"morning:energy:{i}") for i in range(6, 11)]
    buttons.append(row2)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# Вечерние клавиатуры
def kb_evening_done() -> InlineKeyboardMarkup:
    """Клавиатура выполненных задач."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Завершил проект", callback_data="evening:done:0")],
            [InlineKeyboardButton(text="Изучил новое", callback_data="evening:done:1")],
            [InlineKeyboardButton(text="Позанимался спортом", callback_data="evening:done:2")],
            [InlineKeyboardButton(text="Встретился с друзьями", callback_data="evening:done:3")],
            [InlineKeyboardButton(text="✍️ Свой вариант", callback_data="evening:done:custom")]
        ]
    )


def kb_evening_not_done() -> InlineKeyboardMarkup:
    """Клавиатура невыполненных задач."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Не хватило времени", callback_data="evening:not_done:0")],
            [InlineKeyboardButton(text="Было сложно", callback_data="evening:not_done:1")],
            [InlineKeyboardButton(text="Отвлекся", callback_data="evening:not_done:2")],
            [InlineKeyboardButton(text="Устал", callback_data="evening:not_done:3")],
            [InlineKeyboardButton(text="✍️ Свой вариант", callback_data="evening:not_done:custom")]
        ]
    )


def kb_evening_learning() -> InlineKeyboardMarkup:
    """Клавиатура обучения."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Новый навык", callback_data="evening:learning:0")],
            [InlineKeyboardButton(text="Лучше понял себя", callback_data="evening:learning:1")],
            [InlineKeyboardButton(text="Улучшил процесс", callback_data="evening:learning:2")],
            [InlineKeyboardButton(text="Познакомился с людьми", callback_data="evening:learning:3")],
            [InlineKeyboardButton(text="✍️ Свой вариант", callback_data="evening:learning:custom")]
        ]
    )
