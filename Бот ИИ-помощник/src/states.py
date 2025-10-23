"""FSM состояния для бота."""
from aiogram.fsm.state import State, StatesGroup


class Profile(StatesGroup):
    """Состояния для создания профиля (10 вопросов)."""
    q1 = State()  # Время пробуждения
    q2 = State()  # Мотивация
    q3 = State()  # Сильные стороны
    q4 = State()  # Слабость
    q5 = State()  # Длительность фокуса
    q6 = State()  # Стресс
    q7 = State()  # Стиль общения
    q8 = State()  # Идеальное утро
    q9 = State()  # Идеальный вечер
    q10 = State()  # Цель на неделю
    persona = State()  # Выбор персоны


class Morning(StatesGroup):
    """Состояния для утреннего опроса."""
    goal = State()  # Главная цель дня
    goal_text = State()  # Текстовый ввод цели
    top3 = State()  # Топ-3 приоритета
    top3_text = State()  # Текстовый ввод задач
    energy = State()  # Уровень энергии


class Evening(StatesGroup):
    """Состояния для вечернего опроса."""
    done = State()  # Что выполнили
    done_text = State()  # Текстовый ввод выполненных задач
    not_done = State()  # Что не выполнили
    not_done_text = State()  # Текстовый ввод невыполненных задач
    learning = State()  # Что узнали
    learning_text = State()  # Текстовый ввод обучения


class Focus(StatesGroup):
    """Состояния для фокус-сессий."""
    selecting = State()  # Выбор продолжительности
    task = State()  # Ввод задачи
    running = State()  # Активная сессия
    reflection = State()  # Рефлексия после сессии


class Habits(StatesGroup):
    """Состояния для управления привычками."""
    add = State()  # Добавление привычки
    remove = State()  # Удаление привычки
    tick = State()  # Отметка привычки
    rename = State()  # Переименование привычки


class Mood(StatesGroup):
    """Состояния для настроения."""
    energy = State()  # Уровень энергии
    mood = State()  # Уровень настроения
    note = State()  # Заметка о настроении
    note_text = State()  # Ввод текста заметки


class Reflect(StatesGroup):
    """Состояния для рефлексии."""
    topic = State()  # Выбор темы
    prompt = State()  # Ввод вопроса для рефлексии


class Settings(StatesGroup):
    """Состояния для настроек."""
    tz = State()  # Часовой пояс
    time = State()  # Время утра/вечера
    language = State()  # Язык
    persona = State()  # Персона
    clear = State()  # Очистка памяти


class Abstinence(StatesGroup):
    """Состояния для воздержания."""
    add = State()  # Добавление воздержания
