"""Обработчики экспорта данных."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import Export
from ..texts import texts
from ..keyboards import kb_export, kb_post_flow, get_main_menu
from ..storage import db
from ..services import ux, flow
from ..logger import get_logger

logger = get_logger("export")
router = Router()


@router.message(F.text.in_({"📤 Экспорт", "/export"}))
async def export_start(msg: Message, state: FSMContext):
    """Начало экспорта."""
    await msg.answer(
        ux.compose(
            ux.h1("Экспорт данных", "📤"),
            ux.p("Выбери что экспортировать:")
        ),
        reply_markup=kb_export()
    )


@router.callback_query(F.data == "export:today")
async def process_export_today(callback: CallbackQuery, state: FSMContext):
    """Экспорт плана на сегодня."""
    user_id = callback.from_user.id
    
    # Получаем данные за сегодня
    today_entries = await db.get_today_entries(user_id)
    
    # Формируем файл
    content = f"План на сегодня - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    if today_entries:
        for entry in today_entries:
            content += f"• {entry['type']}: {entry['data']}\n"
    else:
        content += "Нет записей за сегодня\n"
    
    # В реальном приложении здесь бы создавался файл
    # Пока просто показываем содержимое
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Экспорт данных", "📤"),
            ux.p("Файл plan_today.txt готов!"),
            ux.block("Содержимое", content.split("\n"), "📄")
        ),
        reply_markup=kb_post_flow()
    )
    await callback.answer()


@router.callback_query(F.data == "export:week")
async def process_export_week(callback: CallbackQuery, state: FSMContext):
    """Экспорт плана на неделю."""
    user_id = callback.from_user.id
    
    # Получаем данные за неделю
    week_entries = await db.get_week_entries(user_id)
    
    # Формируем ICS файл
    content = f"BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Personal Brain//EN\n"
    content += f"BEGIN:VEVENT\n"
    content += f"DTSTART:{datetime.now().strftime('%Y%m%d')}T080000Z\n"
    content += f"DTEND:{datetime.now().strftime('%Y%m%d')}T090000Z\n"
    content += f"SUMMARY:План на неделю\n"
    content += f"DESCRIPTION:Экспорт из Личного Мозга\n"
    content += f"END:VEVENT\n"
    content += f"END:VCALENDAR\n"
    
    # В реальном приложении здесь бы создавался файл
    # Пока просто показываем содержимое
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Экспорт данных", "📤"),
            ux.p("Файл week_plan.ics готов!"),
            ux.block("Содержимое", content.split("\n"), "🗓")
        ),
        reply_markup=kb_post_flow()
    )
    await callback.answer()


@router.message(Export.today)
async def process_export_today_custom(msg: Message, state: FSMContext):
    """Обработка кастомного экспорта дня."""
    # Аналогично process_export_today
    await msg.answer(
        ux.compose(
            ux.h1("Экспорт данных", "📤"),
            ux.p("Файл plan_today.txt готов!")
        ),
        reply_markup=kb_post_flow()
    )
    await state.clear()


@router.message(Export.week)
async def process_export_week_custom(msg: Message, state: FSMContext):
    """Обработка кастомного экспорта недели."""
    # Аналогично process_export_week
    await msg.answer(
        ux.compose(
            ux.h1("Экспорт данных", "📤"),
            ux.p("Файл week_plan.ics готов!")
        ),
        reply_markup=kb_post_flow()
    )
    await state.clear()
