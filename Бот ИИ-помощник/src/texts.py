"""Тексты и сообщения бота."""
from typing import Dict, Any


class Texts:
    """Класс с текстами бота."""
    
    # Приветствие и начало
    WELCOME = """🧠 Привет! Я — твой Личный Мозг.

Помогу планировать день, фокусироваться и расти. Начнём с короткого профиля?"""
    
    PROFILE_START = """📝 Создадим твой психологический профиль.

Ответь на 10 вопросов — это поможет мне лучше понимать тебя и давать персональные советы."""
    
    PROFILE_COMPLETE = """✅ Профиль создан!

Теперь я знаю тебя лучше и смогу давать более точные советы."""
    
    # Утренний опрос
    MORNING_GOAL = """🌅 Доброе утро!

Какая у тебя главная цель на сегодня?"""
    
    MORNING_TOP3 = """🎯 Отлично! Теперь выбери топ-3 приоритета на сегодня."""
    
    MORNING_ENERGY = """⚡ Какой у тебя уровень энергии? (1-10)"""
    
    MORNING_PLAN = """📋 Вот твой план на день:

{plan}

Удачи! 🚀"""
    
    # Вечерний опрос
    EVENING_DONE = """🌙 Добрый вечер!

Что ты выполнил из запланированного?"""
    
    EVENING_NOT_DONE = """📝 Что не удалось выполнить?"""
    
    EVENING_LEARNING = """💡 Что нового ты узнал сегодня?"""
    
    EVENING_REFLECTION = """🤔 Твоя вечерняя рефлексия:

{reflection}

Спокойной ночи! 😴"""
    
    # Фокус-сессии
    FOCUS_SELECT = """🎯 Выбери продолжительность фокус-сессии:"""
    
    FOCUS_RUNNING = """⏰ Фокус-сессия: {duration} мин

{time_left} осталось

Что делаешь: {task}"""
    
    FOCUS_COMPLETE = """✅ Фокус-сессия завершена!

Отличная работа! 🎉"""
    
    FOCUS_PAUSED = """⏸️ Фокус-сессия приостановлена"""
    
    FOCUS_STOPPED = """⏹️ Фокус-сессия остановлена"""
    
    # Привычки
    HABITS_EMPTY = """🔥 У тебя пока нет привычек.

Добавь первую привычку!"""
    
    HABITS_LIST = """🔥 Твои привычки:

{habits}"""
    
    HABIT_ADD = """➕ Введи название новой привычки:"""
    
    HABIT_REMOVE = """🗑️ Какую привычку удалить?"""
    
    HABIT_TICKED = """✅ Привычка отмечена!

Streak: {streak} дней 🔥"""
    
    # Настроение
    MOOD_ENERGY = """⚡ Какой у тебя уровень энергии? (1-10)"""
    
    MOOD_MOOD = """😊 Как твоё настроение? (1-10)"""
    
    MOOD_NOTE = """💭 Хочешь добавить заметку? (или отправь /skip)"""
    
    MOOD_SAVED = """✅ Настроение сохранено!"""
    
    # Рефлексия
    REFLECT_PROMPT = """🧩 Добро пожаловать в диалог с цифровым Я!

Задавай любые вопросы - я готов обсудить всё, что тебя волнует. Можешь спрашивать о целях, проблемах, планах, отношениях или просто поговорить.

Что хочешь обсудить?"""
    
    # Утренние пресеты
    MORNING_GOAL_PRESETS = [
        "Работа над проектом",
        "Изучение нового", 
        "Физическая активность",
        "Встречи и общение",
        "Отдых и восстановление"
    ]
    
    MORNING_TASKS_PRESETS = [
        "Планирование",
        "Кодинг", 
        "Изучение",
        "Встречи",
        "Спорт"
    ]
    
    # Вечерние пресеты
    EVENING_DONE_PRESETS = [
        "Завершил проект",
        "Изучил новое",
        "Позанимался спортом", 
        "Встретился с друзьями"
    ]
    
    EVENING_NOT_DONE_PRESETS = [
        "Не хватило времени",
        "Было сложно",
        "Отвлекся",
        "Устал"
    ]
    
    EVENING_LEARNING_PRESETS = [
        "Новый навык",
        "Лучше понял себя",
        "Улучшил процесс",
        "Познакомился с людьми"
    ]
    
    REFLECT_RESPONSE = """🤖 Ответ цифрового Я:

{response}"""
    
    # Отчеты
    WEEKLY_REPORT = """📊 Твой еженедельный отчет:

{report}"""
    
    WEEKLY_PDF = """📄 PDF отчет готов!

{report}"""
    
    # Настройки
    SETTINGS_MENU = """⚙️ Настройки:

🌍 Часовой пояс: {tz}
🌅 Утренний опрос: {morning_hour}:00
🌙 Вечерний опрос: {evening_hour}:00
🗣️ Язык: {language}
👤 Персона: {persona}"""
    
    # Подписка
    SUBSCRIPTION_FREE = """💳 Твой план: Free

Доступно:
• Базовые привычки (до 2)
• 1 фокус-сессия в день
• Утренний/вечерний опрос
• Базовые отчеты

3-дневный trial Pro активен!"""
    
    SUBSCRIPTION_PRO = """💳 Твой план: Pro

Доступно:
• Полный анализ и профиль
• Неограниченные привычки
• Неограниченные фокус-сессии
• Детальные отчеты
• Персональные советы

Действует до: {expires}"""
    
    SUBSCRIPTION_MENTOR = """💳 Твой план: Mentor

Доступно:
• Все функции Pro
• Диалог "Цифровое Я"
• Углубленные рефлексии
• Расширенная память

Действует до: {expires}"""
    
    SUBSCRIPTION_ULTIMATE = """💳 Твой план: Ultimate

Доступно:
• Все функции Mentor
• PDF отчеты
• Расширенная память
• Улучшенный эмо-анализ

Действует до: {expires}"""
    
    # Платежи
    PAYWALL = """🔒 Эта функция доступна в платных тарифах.

⚡ Pro — 100 ₽/мес · 1000 ₽/год
🔮 Mentor — 200 ₽/мес · 2000 ₽/год  
🧬 Ultimate — 300 ₽/мес · 3000 ₽/год

Оформи подписку в Tribute — мгновенно и безопасно."""
    
    PAYMENT_SUCCESS = """✅ {plan} ({period}) активна до {date}.

Спасибо, что выбрал Личный Мозг! 🎉"""
    
    PAYMENT_FAILED = """❌ Оплата не прошла.

Попробуй еще раз или обратись в поддержку."""
    
    # Ошибки
    ERROR_GENERAL = """❌ Произошла ошибка.

Попробуй еще раз или обратись в поддержку."""
    
    ERROR_COOLDOWN = """⏰ Подожди {seconds} секунд перед следующим запросом."""
    
    ERROR_NOT_FOUND = """❌ Не найдено."""
    
    ERROR_INVALID_INPUT = """❌ Неверный ввод.

Попробуй еще раз."""
    
    # Кнопки
    BUTTON_YES = "✅ Да"
    BUTTON_NO = "❌ Нет"
    BUTTON_SKIP = "⏭️ Пропустить"
    BUTTON_CANCEL = "❌ Отмена"
    BUTTON_BACK = "⬅️ Назад"
    BUTTON_MENU = "🏠 Главное меню"
    
    # Главное меню
    BUTTON_DAY = "📅 Мой день"
    BUTTON_FOCUS = "🎯 Фокус-сессия"
    BUTTON_HABITS = "🔥 Привычки"
    BUTTON_MOOD = "😊 Настроение"
    BUTTON_REFLECT = "🧩 Цифровое Я"
    BUTTON_WEEKLY = "📊 Отчёт недели"
    BUTTON_ABSTINENCE = "🚫 Воздержание"
    BUTTON_SETTINGS = "⚙️ Настройки"
    BUTTON_BILLING = "💳 Подписка"
    
    # Фокус-сессии
    BUTTON_25_MIN = "🍅 25 мин"
    BUTTON_45_MIN = "🔥 45 мин"
    BUTTON_PAUSE = "⏸️ Пауза"
    BUTTON_STOP = "⏹️ Стоп"
    BUTTON_DONE = "✅ Готово"
    
    # Привычки
    BUTTON_ADD_HABIT = "➕ Добавить"
    BUTTON_REMOVE_HABIT = "🗑️ Удалить"
    BUTTON_TICK_HABIT = "✅ Отметить"
    
    # Настроение
    BUTTON_ENERGY_1 = "1"
    BUTTON_ENERGY_2 = "2"
    BUTTON_ENERGY_3 = "3"
    BUTTON_ENERGY_4 = "4"
    BUTTON_ENERGY_5 = "5"
    BUTTON_ENERGY_6 = "6"
    BUTTON_ENERGY_7 = "7"
    BUTTON_ENERGY_8 = "8"
    BUTTON_ENERGY_9 = "9"
    BUTTON_ENERGY_10 = "10"
    
    # Кнопки настроения
    BUTTON_MOOD_1 = "1"
    BUTTON_MOOD_2 = "2"
    BUTTON_MOOD_3 = "3"
    BUTTON_MOOD_4 = "4"
    BUTTON_MOOD_5 = "5"
    BUTTON_MOOD_6 = "6"
    BUTTON_MOOD_7 = "7"
    BUTTON_MOOD_8 = "8"
    BUTTON_MOOD_9 = "9"
    BUTTON_MOOD_10 = "10"
    
    # Тарифы
    BUTTON_FREE = "🧠 Free"
    BUTTON_PRO = "⚡ Pro"
    BUTTON_MENTOR = "🔮 Mentor"
    BUTTON_ULTIMATE = "🧬 Ultimate"
    BUTTON_MONTHLY = "📅 Месяц"
    BUTTON_YEARLY = "📆 Год"
    BUTTON_BUY = "💳 Оплатить"
    BUTTON_CHECK = "🔍 Проверить оплату"
    
    # Персоны
    BUTTON_MENTOR = "🎓 Ментор"
    BUTTON_COACH = "🏃 Коуч"
    BUTTON_FRIEND = "👥 Друг"
    BUTTON_ANALYST = "📊 Аналитик"

    # Подписка
    SUBSCRIBE_TITLE = "Выберите тариф"
    SUBSCRIBE_DESC = "Демонстрационный режим - оплата временно отключена"
    SUBSCRIBE_PLANS = {
        "pro":   {"name": "Pro",      "desc": "Полный анализ, профиль, отчёты, советы", "month": 100, "year": 1000},
        "mentor":{"name": "Mentor",   "desc": "Pro + диалог 'Цифровое Я'", "month": 200, "year": 2000},
        "ult":   {"name": "Ultimate", "desc": "Mentor + PDF-отчёты, расширенная память", "month": 300, "year": 3000}
    }
    DEMO_PAYMENT_DISABLED = "Оплата временно отключена. Это демо-версия. Выберите другой раздел."
    DEMO_PAYMENT_HINT = "Скоро добавим оплату по ссылке (СБП/эквайринг)."
    
    # Завершение потоков
    FLOW_DONE_TITLE = "Готово"
    FLOW_DONE_INTRO_DEFAULT = "Отлично! Я всё запомнил. Встретимся вечером для подведения итогов."
    FLOW_DONE_TIPS_DEFAULT = [
        "Посмотри краткую статистику за сегодня",
        "Запусти фокус-сессию на 25 минут",
        "Вернись в меню, чтобы выбрать другой раздел"
    ]
    FLOW_DONE_FOOTER = "Если хочешь, можешь дополнить заметками позже — я учту в отчёте."
    
    # Отмена
    CANCELLED_TITLE = "Действие отменено"
    CANCELLED_TEXT = "Окей, ничего не сохраняю. Готов продолжить, когда будешь готов."
    
    # Стикеры
    STICKER_WELCOME = "CAACAgIAAxkBAAIBY2Z..."
    STICKER_ENERGY = "CAACAgIAAxkBAAIBZGZ..."
    STICKER_FOCUS = "CAACAgIAAxkBAAIBZWZ..."
    STICKER_SUCCESS = "CAACAgIAAxkBAAIBZmZ..."
    STICKER_MOOD = "CAACAgIAAxkBAAIBZ2Z..."
    
    # Профиль 10Q
    PROFILE_Q1 = "🌅 В какое время ты обычно просыпаешься?"
    PROFILE_Q2 = "💪 Что тебя больше всего мотивирует?"
    PROFILE_Q3 = "⭐ Назови свои 3 сильные стороны"
    PROFILE_Q4 = "🎯 Какая у тебя главная слабость?"
    PROFILE_Q5 = "⏰ Какую длительность фокус-сессии предпочитаешь?"
    PROFILE_Q6 = "😰 Как часто испытываешь стресс?"
    PROFILE_Q7 = "🗣️ Какой стиль общения тебе ближе?"
    PROFILE_Q8 = "🌅 Опиши своё идеальное утро"
    PROFILE_Q9 = "🌙 Опиши свой идеальный вечер"
    PROFILE_Q10 = "🎯 Какая у тебя цель на эту неделю?"
    
    # Варианты ответов для профиля
    PROFILE_A1 = ["06:00-07:00", "07:00-08:00", "08:00-09:00", "09:00-10:00", "10:00+"]
    PROFILE_A2 = ["Достижения", "Признание", "Деньги", "Развитие", "Семья"]
    PROFILE_A3 = ["Аналитичность", "Креативность", "Коммуникабельность", "Лидерство", "Терпение"]
    PROFILE_A4 = ["Прокрастинация", "Перфекционизм", "Неуверенность", "Импульсивность", "Лень"]
    PROFILE_A5 = ["15 минут", "25 минут", "45 минут", "60+ минут"]
    PROFILE_A6 = ["Редко", "Иногда", "Часто", "Постоянно"]
    PROFILE_A7 = ["Прямой", "Мягкий", "Поддерживающий", "Строгий"]
    PROFILE_A8 = ["Спорт + кофе", "Медитация", "Планирование", "Чтение"]
    PROFILE_A9 = ["Релакс", "Общение", "Хобби", "Планирование"]
    PROFILE_A10 = ["Карьера", "Здоровье", "Отношения", "Саморазвитие"]
    
    # Утро - кнопочные варианты
    MORNING_GOAL_PRESETS = [
        "Завершить важный проект",
        "Изучить новую тему", 
        "Встретиться с командой",
        "Провести анализ данных",
        "Подготовить презентацию"
    ]
    MORNING_GOAL_CUSTOM = "✍️ Свой вариант"
    
    MORNING_TASKS_PRESETS = [
        "Проверить почту",
        "Создать план дня",
        "Сделать звонки",
        "Обработать документы", 
        "Подготовить отчет",
        "Встреча с клиентом"
    ]
    MORNING_TASKS_ADD = "✍️ Добавить свои"
    
    # Вечер - кнопочные варианты
    EVENING_DONE_PRESETS = [
        "Завершил важную задачу",
        "Изучил новую информацию",
        "Провел продуктивную встречу",
        "Решил сложную проблему",
        "Помог коллеге"
    ]
    EVENING_DONE_CUSTOM = "✍️ Свой пункт"
    
    EVENING_NOT_DONE_PRESETS = [
        "Не хватило времени",
        "Технические проблемы",
        "Отвлекли коллеги",
        "Сложность задачи",
        "Усталость"
    ]
    EVENING_NOT_DONE_CUSTOM = "✍️ Свой"
    
    EVENING_LEARNING_PRESETS = [
        "Новый способ решения",
        "Работа с инструментами",
        "Командная работа",
        "Тайм-менеджмент",
        "Технические навыки"
    ]
    EVENING_LEARNING_CUSTOM = "✍️ Свой"
    
    # Настроение - только кнопки
    MOOD_ENERGY_TITLE = "⚡ Какой у тебя уровень энергии?"
    MOOD_FEEL_TITLE = "😊 Как твоё настроение?"
    MOOD_NOTE_TITLE = "💭 Хочешь добавить заметку?"
    MOOD_NOTE_ADD = "📝 Добавить заметку"
    MOOD_NOTE_SKIP = "⏭ Пропустить"
    
    # Фокус-сессия
    FOCUS_DURATION_TITLE = "🎯 Выбери длительность фокус-сессии"
    FOCUS_25_MIN = "🍅 25 минут"
    FOCUS_45_MIN = "🔥 45 минут"
    FOCUS_TASK_PROMPT = "🎯 Что будешь делать во время фокус-сессии?"
    
    FOCUS_REFLECTION_TITLE = "Как прошла сессия?"
    FOCUS_REFLECTION_PRESETS = [
        "Очень продуктивно",
        "Нормально, но отвлекался", 
        "Сложно было сосредоточиться"
    ]
    FOCUS_REFLECTION_CUSTOM = "✍️ Свой"
    
    # Привычки
    HABITS_LIST_TITLE = "🔥 Твои привычки"
    HABITS_ADD_TITLE = "➕ Добавить привычку"
    HABITS_RENAME_TITLE = "✏️ Переименовать привычку"
    HABITS_DELETE_TITLE = "🗑️ Удалить привычку"
    HABITS_TICK_TITLE = "✅ Отметить привычку"
    
    # Цифровое Я
    REFLECT_TOPICS_TITLE = "🧩 О чём поговорим?"
    REFLECT_TOPICS = [
        "Мотивация и цели",
        "Прокрастинация",
        "Фокус и концентрация", 
        "Стресс и усталость"
    ]
    REFLECT_TOPICS_CUSTOM = "✍️ Свой вопрос"
    
    REFLECT_ACTIONS = [
        "🔁 Уточнить",
        "📌 Запомнить инсайт", 
        "↩️ В меню"
    ]
    
    # Настройки
    SETTINGS_TZ_TITLE = "🌍 Часовой пояс"
    SETTINGS_TZ_POPULAR = [
        "Europe/Moscow",
        "Europe/London", 
        "America/New_York",
        "Asia/Tokyo"
    ]
    SETTINGS_TZ_CUSTOM = "✍️ Ввести свой"
    
    SETTINGS_TIME_TITLE = "⏰ Время утра/вечера"
    SETTINGS_TIME_MORNING = "🌅 Утро"
    SETTINGS_TIME_EVENING = "🌙 Вечер"
    SETTINGS_TIME_ADJUST = ["-15", "-5", "+5", "+15"]
    
    SETTINGS_LANGUAGE_TITLE = "🗣️ Язык"
    SETTINGS_LANGUAGE_RU = "🇷🇺 Русский"
    SETTINGS_LANGUAGE_EN = "🇺🇸 English"
    
    SETTINGS_PERSONA_TITLE = "👤 Персона"
    SETTINGS_PERSONA_MENTOR = "🧙 Наставник"
    SETTINGS_PERSONA_COACH = "🚀 Коуч"
    SETTINGS_PERSONA_FRIEND = "🤝 Друг"
    SETTINGS_PERSONA_ANALYST = "🧘 Аналитик"
    
    SETTINGS_CLEAR_TITLE = "🧹 Очистить память"
    SETTINGS_CLEAR_CONFIRM = "Удалить данные за 7 дней?"
    SETTINGS_CLEAR_YES = "Да, удалить"
    SETTINGS_CLEAR_NO = "Нет, оставить"
    
    # Подписка - демо
    SUBSCRIBE_DEMO_TITLE = "💳 Подписка"
    SUBSCRIBE_DEMO_DISABLED = "⏳ Оплата временно отключена. Это демо-версия."
    SUBSCRIBE_DEMO_FEATURES = "Что получу?"
    
    # Экспорт
    EXPORT_TITLE = "📤 Экспорт данных"
    EXPORT_TODAY = "📄 plan_today.txt"
    EXPORT_WEEK = "🗓 week_plan.ics"
    EXPORT_READY = "Файл готов"


# Глобальный экземпляр текстов
texts = Texts()
