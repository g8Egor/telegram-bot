"""Обработчики команды /start."""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..states import Profile
from ..storage import db, User
from ..texts import texts
from ..keyboards import kb_profile_q1, get_main_menu
from ..logger import get_logger
from datetime import datetime, timedelta
from ..services import ux

logger = get_logger("start")
router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start."""
    user_id = message.from_user.id
    
    # Проверяем, есть ли пользователь в базе
    user = await db.get_user(user_id)
    
    if user is None:
        # Создаем нового пользователя
        new_user = User(
            tg_id=user_id,
            created_at=datetime.now(),
            plan_tier="free",
            trial_until=datetime.now() + timedelta(days=5)  # 5-дневный trial
        )
        await db.upsert_user(new_user)
        logger.info(f"New user created: {user_id}")
        
        # Начинаем создание профиля
        # await message.answer_sticker(texts.STICKER_WELCOME)  # Временно отключено
        await message.answer(
            ux.compose(
                ux.h1("Добро пожаловать!", "🧠"),
                ux.p("Я — твой Личный Мозг! Помогу планировать день, фокусироваться и расти."),
                ux.block("Начнём с короткого профиля?", ["Создадим твой психологический портрет", "Это займёт всего 2 минуты"], "✨")
            )
        )
        
        await message.answer(
            ux.compose(
                ux.h1("Профиль", "📝"),
                ux.p(texts.PROFILE_START)
            )
        )
        await message.answer(
            ux.compose(
                ux.h1("Профиль", "📝"),
                ux.p(texts.PROFILE_Q1)
            ),
            reply_markup=kb_profile_q1()
        )
        await state.set_state(Profile.q1)
    else:
        # Пользователь уже существует
        return_pretty = ux.compose(
            ux.h1("Привет! Рад видеть тебя снова!", "🎉"),
            ux.p("Твой профиль готов, все функции доступны!"),
            ux.block("Что будем делать?", ["Планировать день", "Фокусироваться", "Отслеживать прогресс"], "🚀")
        )
        
        await message.answer(return_pretty, reply_markup=get_main_menu())
        await state.clear()


@router.message(Profile.q1, F.text == texts.BUTTON_YES)
async def start_profile(message: Message, state: FSMContext):
    """Начинает создание профиля."""
    await message.answer(
        texts.PROFILE_START,
        reply_markup=None
    )
    await message.answer(
        "1. Как бы вы описали свой характер?",
        reply_markup=None
    )
    await state.set_state(Profile.q1)


@router.message(Profile.q1, F.text == texts.BUTTON_NO)
async def skip_profile(message: Message, state: FSMContext):
    """Пропускает создание профиля."""
    await message.answer(
        "Хорошо, профиль можно будет создать позже в настройках.",
        reply_markup=get_main_menu()
    )
    await state.clear()


@router.message(Profile.q1)
async def process_q1(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 1."""
    await state.update_data(q1=message.text)
    await message.answer("2. Что вас больше всего мотивирует?")
    await state.set_state(Profile.q2)


@router.message(Profile.q2)
async def process_q2(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 2."""
    await state.update_data(q2=message.text)
    await message.answer("3. Как вы предпочитаете работать?")
    await state.set_state(Profile.q3)


@router.message(Profile.q3)
async def process_q3(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 3."""
    await state.update_data(q3=message.text)
    await message.answer("4. Что для вас означает успех?")
    await state.set_state(Profile.q4)


@router.message(Profile.q4)
async def process_q4(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 4."""
    await state.update_data(q4=message.text)
    await message.answer("5. Как вы справляетесь со стрессом?")
    await state.set_state(Profile.q5)


@router.message(Profile.q5)
async def process_q5(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 5."""
    await state.update_data(q5=message.text)
    await message.answer("6. Что вас больше всего беспокоит?")
    await state.set_state(Profile.q6)


@router.message(Profile.q6)
async def process_q6(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 6."""
    await state.update_data(q6=message.text)
    await message.answer("7. Как вы предпочитаете общаться?")
    await state.set_state(Profile.q7)


@router.message(Profile.q7)
async def process_q7(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 7."""
    await state.update_data(q7=message.text)
    await message.answer("8. Что для вас важно в отношениях?")
    await state.set_state(Profile.q8)


@router.message(Profile.q8)
async def process_q8(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 8."""
    await state.update_data(q8=message.text)
    await message.answer("9. Как вы принимаете решения?")
    await state.set_state(Profile.q9)


@router.message(Profile.q9)
async def process_q9(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 9."""
    await state.update_data(q9=message.text)
    await message.answer("10. Что вы хотели бы изменить в себе?")
    await state.set_state(Profile.q10)


@router.message(Profile.q10)
async def process_q10(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 10 и завершает профиль."""
    await state.update_data(q10=message.text)
    
    # Получаем все ответы
    data = await state.get_data()
    
    # Создаем профиль через GPT
    from ..services.gpt import gpt_service
    profile = await gpt_service.build_profile(data)
    
    # Сохраняем профиль в базу
    import json
    await db._connection.execute("""
        INSERT OR REPLACE INTO profiles (tg_id, data)
        VALUES (?, ?)
    """, (message.from_user.id, json.dumps(profile)))
    await db._connection.commit()
    
    # Показываем краткий портрет
    from ..services import ux
    
    profile_parts = [
        f"👤 Тип: {profile.get('personality_type', 'Не определен')}",
        f"💪 Сильные стороны: {', '.join(profile.get('strengths', []))}",
        f"🎯 Области роста: {', '.join(profile.get('growth_areas', []))}",
        f"💬 Стиль общения: {profile.get('communication_style', 'Не определен')}",
        f"🚀 Мотивация: {', '.join(profile.get('motivation_factors', []))}"
    ]
    
    profile_pretty = ux.compose(
        ux.h1("Твой психологический портрет", "🧠"),
        ux.block("Анализ личности", profile_parts, "📊"),
        ux.hr(),
        ux.p("Отлично! Теперь я знаю, как лучше тебе помочь. Начнём работу! 🚀")
    )
    
    await message.answer(profile_pretty, reply_markup=get_main_menu())
    
    await state.clear()
    logger.info(f"Profile completed for user {message.from_user.id}")
