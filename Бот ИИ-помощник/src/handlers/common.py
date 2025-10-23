"""Общие обработчики (отмена, навигация)."""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from ..services import ux, flow
from ..keyboards import get_main_menu
from .. import texts

router = Router(name=__name__)


@router.message(F.text.casefold() == "/cancel")
@router.message(F.text == "❌ Отмена")
async def cancel_any(msg: Message, state: FSMContext):
    """Универсальная отмена для всех FSM."""
    await state.clear()
    await msg.answer(
        flow.finish_card(texts.CANCELLED_TITLE, texts.CANCELLED_TEXT),
        reply_markup=get_main_menu()
    )


@router.callback_query(F.data == "nav:menu")
async def return_to_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню."""
    await state.clear()
    await callback.message.answer(
        ux.compose(
            ux.h1("Главное меню", "🏠"),
            ux.p("Выбери раздел:")
        ),
        reply_markup=get_main_menu()
    )
    await callback.answer()
