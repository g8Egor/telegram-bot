"""Обработчики еженедельных отчетов."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..texts import texts
from ..keyboards import kb_post_flow, get_main_menu
from ..storage import db
from ..services.reports import report_service
from ..services.pdf import pdf_service
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("weekly")
router = Router()


@router.message(F.text == texts.BUTTON_WEEKLY)
async def cmd_weekly(message: Message, state: FSMContext):
    """Обработчик кнопки 'Отчёт недели'."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer(texts.ERROR_NOT_FOUND)
        return
    
    # Генерируем отчет
    report = await report_service.generate_weekly_report(user_id, user.persona)
    
    # Форматируем ответ красиво
    summary_lines = report.split("\n")
    
    pretty = ux.compose(
        ux.h1("Отчёт недели", "📊"),
        ux.block("Короткий обзор", summary_lines, "📆", footer="Продолжаем держать темп!"),
        ux.hr()
    )
    
    await message.answer(pretty)
    
    # Добавляем finish-карточку
    await message.answer(
        flow.finish_card(
            title=texts.FLOW_DONE_TITLE,
            intro="Отчет готов! Проанализируй свои достижения.",
            tips=["Экспортируй в PDF", "Поделись результатами", "Вернись в меню"],
            footer="Отличная работа на этой неделе!"
        ),
        reply_markup=kb_post_flow()
    )
    
    logger.info(f"Weekly report generated for user {user_id}")


@router.message(F.text == "/export_pdf")
async def cmd_export_pdf(message: Message, state: FSMContext):
    """Обработчик экспорта PDF отчета."""
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await message.answer(texts.ERROR_NOT_FOUND)
        return
    
    # Проверяем план пользователя и пробный период
    from datetime import datetime
    if user.plan_tier != "ultimate":
        # Проверяем пробный период
        if user.trial_until and user.trial_until > datetime.now():
            # Пробный период активен - разрешаем PDF
            pass
        else:
            await message.answer(
                "❌ PDF отчеты доступны только в тарифе Ultimate.\n\n"
                "Обновите подписку для доступа к этой функции.",
                reply_markup=get_main_menu()
            )
            return
    
    # Генерируем PDF
    try:
        pdf_path = await pdf_service.generate_weekly_pdf(
            user_id=user_id,
            user_name=message.from_user.first_name or "Пользователь"
        )
        
        # Отправляем файл
        from aiogram.types import FSInputFile
        pdf_file = FSInputFile(pdf_path)
        
        await message.answer_document(
            document=pdf_file,
            caption="📄 Ваш еженедельный PDF отчет готов!"
        )
        
        # Добавляем finish-карточку
        await message.answer(
            flow.finish_card(
                title="PDF готов",
                intro="Отчет сохранен в PDF формате.",
                tips=["Поделись с друзьями", "Сохрани в облако", "Вернись в меню"],
                footer="Отличная работа!"
            ),
            reply_markup=kb_post_flow()
        )
        
        logger.info(f"PDF report sent to user {user_id}")
        
    except Exception as e:
        logger.error(f"PDF generation error for user {user_id}: {e}")
        await message.answer(
            flow.finish_card(
                title="Ошибка",
                intro="Не удалось сгенерировать PDF. Попробуй позже.",
                tips=["Проверь интернет", "Попробуй снова", "Вернись в меню"]
            ),
            reply_markup=kb_post_flow()
        )


@router.message(F.text == "/export_day")
async def cmd_export_day(message: Message, state: FSMContext):
    """Обработчик экспорта плана дня."""
    user_id = message.from_user.id
    
    # Получаем записи за сегодня
    from datetime import date
    today = date.today().isoformat()
    
    async with db._connection.execute("""
        SELECT type, data FROM entries 
        WHERE tg_id = ? AND date = ?
        ORDER BY created_at ASC
    """, (user_id, today)) as cursor:
        entries = await cursor.fetchall()
    
    if not entries:
        await message.answer(
            flow.finish_card(
                title="Нет данных",
                intro="У вас нет записей за сегодня.",
                tips=["Заполни утренний опрос", "Заполни вечерний опрос", "Вернись в меню"],
                footer="Заполните опросы для создания плана дня."
            ),
            reply_markup=kb_post_flow()
        )
        return
    
    # Формируем план дня
    plan_text = "📅 План дня:\n\n"
    
    for entry_type, data in entries:
        import json
        try:
            data_dict = json.loads(data)
            if entry_type == "morning":
                plan_text += f"🌅 Утренний план:\n"
                plan_text += f"Цель: {data_dict.get('goal', 'Не указано')}\n"
                plan_text += f"Приоритеты: {', '.join(data_dict.get('top3', []))}\n"
                plan_text += f"Энергия: {data_dict.get('energy', 5)}/10\n\n"
            elif entry_type == "evening":
                plan_text += f"🌙 Вечерняя рефлексия:\n"
                plan_text += f"Выполнено: {', '.join(data_dict.get('done', []))}\n"
                plan_text += f"Не выполнено: {', '.join(data_dict.get('not_done', []))}\n"
                plan_text += f"Изучено: {data_dict.get('learning', 'Не указано')}\n\n"
        except json.JSONDecodeError:
            continue
    
    await message.answer(plan_text)
    
    # Добавляем finish-карточку
    await message.answer(
        flow.finish_card(
            title="План готов",
            intro="План дня экспортирован.",
            tips=["Сохрани в заметки", "Поделись с друзьями", "Вернись в меню"],
            footer="Отличная работа!"
        ),
        reply_markup=kb_post_flow()
    )
    
    logger.info(f"Day plan exported for user {user_id}")


@router.message(F.text == "/export_week")
async def cmd_export_week(message: Message, state: FSMContext):
    """Обработчик экспорта календаря недели."""
    user_id = message.from_user.id
    
    # Получаем записи за неделю
    from datetime import datetime, timedelta
    week_ago = (datetime.now() - timedelta(days=7)).date()
    
    async with db._connection.execute("""
        SELECT date, type, data FROM entries 
        WHERE tg_id = ? AND date >= ?
        ORDER BY date ASC, created_at ASC
    """, (user_id, week_ago.isoformat())) as cursor:
        entries = await cursor.fetchall()
    
    if not entries:
        await message.answer(
            flow.finish_card(
                title="Нет данных",
                intro="У вас нет записей за неделю.",
                tips=["Заполни опросы", "Вернись в меню"],
                footer="Заполните опросы для создания календаря недели."
            ),
            reply_markup=kb_post_flow()
        )
        return
    
    # Формируем календарь недели
    calendar_text = "📅 Календарь недели:\n\n"
    
    current_date = None
    for date_str, entry_type, data in entries:
        if current_date != date_str:
            current_date = date_str
            calendar_text += f"📅 {date_str}:\n"
        
        import json
        try:
            data_dict = json.loads(data)
            if entry_type == "morning":
                calendar_text += f"  🌅 Цель: {data_dict.get('goal', 'Не указано')}\n"
            elif entry_type == "evening":
                calendar_text += f"  🌙 Выполнено: {len(data_dict.get('done', []))} задач\n"
        except json.JSONDecodeError:
            continue
    
    await message.answer(calendar_text)
    
    # Добавляем finish-карточку
    await message.answer(
        flow.finish_card(
            title="Календарь готов",
            intro="Календарь недели экспортирован.",
            tips=["Сохрани в заметки", "Поделись с друзьями", "Вернись в меню"],
            footer="Отличная работа!"
        ),
        reply_markup=kb_post_flow()
    )
    
    logger.info(f"Week calendar exported for user {user_id}")


# Обработчики для кнопок в kb_post_flow
@router.callback_query(F.data == "focus:open")
async def process_focus_from_weekly(callback: CallbackQuery, state: FSMContext):
    """Переход к фокус-сессии из отчета."""
    from .focus import focus_start
    await focus_start(callback.message, state)
    await callback.answer()


@router.callback_query(F.data == "nav:stats")
async def process_stats_from_weekly(callback: CallbackQuery, state: FSMContext):
    """Показать статистику дня из отчета."""
    user_id = callback.from_user.id
    
    # Получаем данные за сегодня
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Получаем записи настроения
    async with db._connection.execute("""
        SELECT energy, mood, note FROM mood WHERE tg_id = ? AND date = ?
    """, (user_id, today)) as cursor:
        mood_data = await cursor.fetchone()
    
    # Получаем фокус-сессии
    async with db._connection.execute("""
        SELECT COUNT(*), SUM(duration) FROM pomodoro 
        WHERE tg_id = ? AND DATE(started_at) = ?
    """, (user_id, today)) as cursor:
        focus_data = await cursor.fetchone()
    
    # Получаем привычки
    async with db._connection.execute("""
        SELECT COUNT(*) FROM habits WHERE tg_id = ?
    """, (user_id,)) as cursor:
        habits_count = await cursor.fetchone()
    
    # Формируем статистику
    stats_parts = []
    
    if mood_data:
        stats_parts.append(f"Энергия: {mood_data[0]}/10")
        stats_parts.append(f"Настроение: {mood_data[1]}/10")
        if mood_data[2]:
            stats_parts.append(f"Заметка: {mood_data[2][:50]}...")
    
    if focus_data and focus_data[0] > 0:
        stats_parts.append(f"Фокус-сессий: {focus_data[0]}")
        stats_parts.append(f"Время фокуса: {focus_data[1] or 0} мин")
    
    if habits_count and habits_count[0] > 0:
        stats_parts.append(f"Привычек: {habits_count[0]}")
    
    if not stats_parts:
        stats_text = "Пока нет данных за сегодня"
    else:
        stats_text = "\n".join(stats_parts)
    
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Статистика дня", "📊"),
            ux.p(stats_text)
        ),
        reply_markup=kb_post_flow()
    )
    await callback.answer()
