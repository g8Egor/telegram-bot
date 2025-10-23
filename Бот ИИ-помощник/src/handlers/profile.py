"""Обработчики создания профиля."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import Profile
from ..texts import texts
from ..keyboards import (
    kb_profile_q1, kb_profile_q2, kb_profile_q3, kb_profile_q4, kb_profile_q5,
    kb_profile_q6, kb_profile_q7, kb_profile_q8, kb_profile_q9, kb_profile_q10,
    kb_profile_persona, kb_post_flow, get_main_menu
)
from ..storage import db
from ..services.gpt import gpt_service
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("profile")
router = Router()


@router.message(Profile.q1)
async def process_q1(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 1."""
    await state.update_data(q1=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q2)
        ),
        reply_markup=kb_profile_q2()
    )
    await state.set_state(Profile.q2)


@router.callback_query(F.data.startswith("profile:q1:"))
async def process_q1_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 1."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A1[idx]
    await state.update_data(q1=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q2)
        ),
        reply_markup=kb_profile_q2()
    )
    await callback.answer()


@router.message(Profile.q2)
async def process_q2(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 2."""
    await state.update_data(q2=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q3)
        ),
        reply_markup=kb_profile_q3()
    )
    await state.set_state(Profile.q3)


@router.callback_query(F.data.startswith("profile:q2:"))
async def process_q2_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 2."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A2[idx]
    await state.update_data(q2=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q3)
        ),
        reply_markup=kb_profile_q3()
    )
    await callback.answer()


@router.message(Profile.q3)
async def process_q3(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 3."""
    await state.update_data(q3=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q4)
        ),
        reply_markup=kb_profile_q4()
    )
    await state.set_state(Profile.q4)


@router.callback_query(F.data.startswith("profile:q3:"))
async def process_q3_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 3."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A3[idx]
    await state.update_data(q3=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q4)
        ),
        reply_markup=kb_profile_q4()
    )
    await callback.answer()


@router.message(Profile.q4)
async def process_q4(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 4."""
    await state.update_data(q4=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q5)
        ),
        reply_markup=kb_profile_q5()
    )
    await state.set_state(Profile.q5)


@router.callback_query(F.data.startswith("profile:q4:"))
async def process_q4_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 4."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A4[idx]
    await state.update_data(q4=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q5)
        ),
        reply_markup=kb_profile_q5()
    )
    await callback.answer()


@router.message(Profile.q5)
async def process_q5(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 5."""
    await state.update_data(q5=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q6)
        ),
        reply_markup=kb_profile_q6()
    )
    await state.set_state(Profile.q6)


@router.callback_query(F.data.startswith("profile:q5:"))
async def process_q5_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 5."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A5[idx]
    await state.update_data(q5=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q6)
        ),
        reply_markup=kb_profile_q6()
    )
    await callback.answer()


@router.message(Profile.q6)
async def process_q6(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 6."""
    await state.update_data(q6=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q7)
        ),
        reply_markup=kb_profile_q7()
    )
    await state.set_state(Profile.q7)


@router.callback_query(F.data.startswith("profile:q6:"))
async def process_q6_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 6."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A6[idx]
    await state.update_data(q6=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q7)
        ),
        reply_markup=kb_profile_q7()
    )
    await callback.answer()


@router.message(Profile.q7)
async def process_q7(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 7."""
    await state.update_data(q7=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q8)
        ),
        reply_markup=kb_profile_q8()
    )
    await state.set_state(Profile.q8)


@router.callback_query(F.data.startswith("profile:q7:"))
async def process_q7_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 7."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A7[idx]
    await state.update_data(q7=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q8)
        ),
        reply_markup=kb_profile_q8()
    )
    await callback.answer()


@router.message(Profile.q8)
async def process_q8(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 8."""
    await state.update_data(q8=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q9)
        ),
        reply_markup=kb_profile_q9()
    )
    await state.set_state(Profile.q9)


@router.callback_query(F.data.startswith("profile:q8:"))
async def process_q8_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 8."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A8[idx]
    await state.update_data(q8=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q9)
        ),
        reply_markup=kb_profile_q9()
    )
    await callback.answer()


@router.message(Profile.q9)
async def process_q9(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 9."""
    await state.update_data(q9=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q10)
        ),
        reply_markup=kb_profile_q10()
    )
    await state.set_state(Profile.q10)


@router.callback_query(F.data.startswith("profile:q9:"))
async def process_q9_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 9."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A9[idx]
    await state.update_data(q9=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p(texts.PROFILE_Q10)
        ),
        reply_markup=kb_profile_q10()
    )
    await callback.answer()


@router.message(Profile.q10)
async def process_q10(message: Message, state: FSMContext):
    """Обрабатывает ответ на вопрос 10."""
    await state.update_data(q10=message.text)
    await message.answer(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p("Выбери свою персону:")
        ),
        reply_markup=kb_profile_persona()
    )
    await state.set_state(Profile.persona)


@router.callback_query(F.data.startswith("profile:q10:"))
async def process_q10_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор ответа на вопрос 10."""
    idx = int(callback.data.split(":")[2])
    answer = texts.PROFILE_A10[idx]
    await state.update_data(q10=answer)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль", "📝"),
            ux.p("Выбери свою персону:")
        ),
        reply_markup=kb_profile_persona()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("profile:persona:"))
async def process_persona(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор персоны."""
    persona = callback.data.split(":")[2]
    await state.update_data(persona=persona)
    
    # Получаем все ответы
    data = await state.get_data()
    answers = [data.get(f'q{i}') for i in range(1, 11)]
    
    try:
        # Генерируем профиль через GPT
        profile_data = await gpt_service.build_profile(answers)
        
        # Преобразуем в читаемый текст
        profile_text = f"""🧠 Психологический портрет:

👤 Тип личности: {profile_data.get('personality_type', 'Адаптивный')}

📝 Детальный анализ:
{profile_data.get('detailed_analysis', 'Анализ временно недоступен')}

💪 Сильные стороны:
{chr(10).join('• ' + strength for strength in profile_data.get('strengths', []))}

🎯 Области для развития:
{chr(10).join('• ' + area for area in profile_data.get('growth_areas', []))}

💬 Стиль общения: {profile_data.get('communication_style', 'Дружелюбный')}

🚀 Факторы мотивации:
{chr(10).join('• ' + factor for factor in profile_data.get('motivation_factors', []))}

💡 Персональный совет:
{profile_data.get('personal_advice', 'Совет временно недоступен')}"""
        
        # Сохраняем профиль в базу
        await db.save_profile(callback.from_user.id, profile_text)
        
        # Обновляем персону пользователя
        await db.update_user_persona(callback.from_user.id, persona)
        
        logger.info(f"Profile created successfully for user {callback.from_user.id}")
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        profile_text = "Профиль создан, но анализ временно недоступен."
        await db.save_profile(callback.from_user.id, profile_text)
        await db.update_user_persona(callback.from_user.id, persona)
    
    # Показываем результат
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Профиль создан!", "✅"),
            ux.p("Краткий портрет:"),
            ux.block("Анализ", profile_text.split("\n"), "🧠")
        ),
        reply_markup=None
    )
    
    # Добавляем finish-карточку
    await callback.message.answer(
        flow.finish_card(
            title=texts.FLOW_DONE_TITLE,
            intro="Теперь я знаю тебя лучше и смогу давать более точные советы.",
            tips=["Начни с утреннего опроса", "Попробуй фокус-сессию", "Вернись в меню"],
            footer="Добро пожаловать в Личный Мозг!"
        ),
        reply_markup=kb_post_flow()
    )
    
    await state.clear()
    await callback.answer()
    logger.info(f"Profile created for user {callback.from_user.id}")
