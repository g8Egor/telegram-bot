"""Обработчики подписки через Tribute."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from ..services import ux
from .. import texts
from ..config import config
from ..keyboards import get_main_menu

router = Router(name=__name__)

@router.message(F.text.in_({"💳 Подписка", "/billing", "/subscribe"}))
async def billing_menu(msg: Message):
    """Показывает информацию о подписке Pro."""
    title = ux.h1("Подписка Pro", "💳")
    intro = ux.p("5 дней бесплатно — полный доступ. После 5 дней без Pro будут ограничения на фокус-сессию и \"Цифровое Я\".")
    
    features = [
        "🎯 Неограниченные фокус-сессии (25 и 45 минут)",
        "🧩 Полный доступ к Цифровому Я",
        "📊 Расширенная аналитика",
        "💾 Экспорт данных",
        "🔔 Персональные уведомления"
    ]
    
    body = ux.block("Возможности Pro", features, "✨")
    footer = ux.p("Pro — 199 ₽/мес. 5 дней — бесплатно.")
    
    # Кнопка для оформления в Tribute
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Оформить Pro в Tribute", 
            url=config.tribute_product_url
        )],
        [InlineKeyboardButton(text="↩️ В меню", callback_data="nav:menu")]
    ])
    
    await msg.answer(
        ux.compose(title, intro, body, ux.hr(), footer),
        reply_markup=keyboard
    )

@router.message(F.text.contains("подписка"))
async def billing_menu_alt(msg: Message):
    """Альтернативный обработчик для подписки."""
    await billing_menu(msg)

@router.callback_query(F.data == "nav:menu")
async def back_to_menu(callback: CallbackQuery):
    """Возврат в главное меню."""
    await callback.message.edit_text(
        ux.compose(
            ux.h1("Главное меню", "🏠"),
            ux.p("Выберите раздел:")
        ),
        reply_markup=get_main_menu()
    )
    await callback.answer()