"""Обработчики биллинга (демо-режим)."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from ..services import ux
from .. import texts
from ..keyboards import kb_subscriptions

router = Router(name=__name__)

@router.message(F.text.in_({"💳 Подписка", "/billing", "/subscribe"}))
async def billing_menu(msg: Message):
    title = ux.h1(texts.SUBSCRIBE_TITLE, "💳")
    intro = ux.p(texts.SUBSCRIBE_DESC)
    plans = []
    for key, meta in texts.SUBSCRIBE_PLANS.items():
        plans.append(f"{meta['name']} — {ux.escape(meta['desc'])}")
    body = ux.block("Доступные тарифы", plans, "📦")
    await msg.answer(ux.compose(title, intro, body), reply_markup=kb_subscriptions())

@router.message(F.text.contains("подписка"))
async def billing_menu_alt(msg: Message):
    """Альтернативный обработчик для подписки."""
    title = ux.h1(texts.SUBSCRIBE_TITLE, "💳")
    intro = ux.p(texts.SUBSCRIBE_DESC)
    plans = []
    for key, meta in texts.SUBSCRIBE_PLANS.items():
        plans.append(f"{meta['name']} — {ux.escape(meta['desc'])}")
    body = ux.block("Доступные тарифы", plans, "📦")
    await msg.answer(ux.compose(title, intro, body), reply_markup=kb_subscriptions())

@router.callback_query(F.data.startswith("plan:"))
async def billing_pick_plan(cb: CallbackQuery):
    # data: plan:<tier>:<period>
    _, tier, period = cb.data.split(":")
    meta = texts.SUBSCRIBE_PLANS.get(tier, {"name":"Тариф","desc":"","month":0,"year":0})
    
    # Получаем цену в зависимости от периода
    price = meta.get("month" if period == "month" else "year", 0)
    period_text = "месяц" if period == "month" else "год"
    
    title = ux.h1(f"{meta['name']} — {price} ₽ / {period_text}", "🧾")
    info = ux.p(meta["desc"])
    warn = ux.block("Статус оплаты", [texts.DEMO_PAYMENT_DISABLED], "⏳", footer=texts.DEMO_PAYMENT_HINT)
    await cb.message.answer(ux.compose(title, info, ux.hr(), warn))
    await cb.answer()