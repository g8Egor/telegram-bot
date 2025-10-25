"""Middleware для проверки подписки и trial."""
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime, date

from ..storage import db
from ..texts import texts
from ..config import config
from ..services import ux
from ..logger import get_logger

logger = get_logger("subscription_gate")


class SubscriptionGateMiddleware(BaseMiddleware):
    """Middleware для проверки подписки и trial пользователя."""
    
    def __init__(self):
        # Команды, доступные только с Pro подпиской
        self.pro_commands = {
            "🧩 Цифровое Я",  # Только Pro
            texts.BUTTON_REFLECT
        }
        
        # Команды с ограничениями для Free плана
        self.limited_commands = {
            "🎯 Фокус-сессия",  # 1 сессия 25 минут в день
            texts.BUTTON_FOCUS
        }
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Проверяет подписку и trial перед обработкой сообщения."""
        
        # Получаем ID пользователя
        if isinstance(event, Message):
            user_id = event.from_user.id
            text = event.text
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            text = event.data
        else:
            return await handler(event, data)
        
        # Получаем пользователя
        user = await db.get_user(user_id)
        if not user:
            return await handler(event, data)
        
        # Проверяем trial период
        is_trial_active = user.trial_until and user.trial_until > datetime.now()
        is_pro_active = user.plan_tier == "pro" and user.subscription_until and user.subscription_until > datetime.now()
        
        # Проверяем Pro команды (Цифровое Я)
        if text in self.pro_commands:
            if is_trial_active or is_pro_active:
                # Доступ разрешен
                pass
            else:
                # Показываем paywall для Цифрового Я
                await self._show_digital_self_paywall(event)
                return
        
        # Проверяем ограничения для фокус-сессий
        elif text in self.limited_commands:
            if is_trial_active or is_pro_active:
                # Полный доступ
                return await handler(event, data)
            else:
                # Ограниченный доступ - только 1 сессия 25 минут в день
                if "focus" in text.lower() or "фокус" in text.lower():
                    return await self._check_focus_limits(event, user_id)
        
        # Если все проверки пройдены, продолжаем обработку
        return await handler(event, data)
    
    async def _show_digital_self_paywall(self, event):
        """Показывает paywall для Цифрового Я."""
        title = ux.h1("Цифровое Я", "🧩")
        intro = ux.p("Цифровое Я доступно только в подписке Pro.")
        features = [
            "💭 Персональные диалоги",
            "🧠 Анализ на основе профиля",
            "💡 Конкретные советы",
            "📚 Память о ваших разговорах"
        ]
        body = ux.block("Возможности", features, "✨")
        footer = ux.p("Pro — 199 ₽/мес. 5 дней — бесплатно.")
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Оформить Pro в Tribute", 
                url=config.tribute_product_url
            )],
            [InlineKeyboardButton(text="↩️ В меню", callback_data="nav:menu")]
        ])
        
        if isinstance(event, Message):
            await event.answer(
                ux.compose(title, intro, body, ux.hr(), footer),
                reply_markup=keyboard
            )
        else:
            await event.message.edit_text(
                ux.compose(title, intro, body, ux.hr(), footer),
                reply_markup=keyboard
            )
            await event.answer()
    
    async def _check_focus_limits(self, event, user_id):
        """Проверяет лимиты фокус-сессий."""
        today = date.today().isoformat()
        
        async with db._connection.execute("""
            SELECT COUNT(*) FROM pomodoro 
            WHERE tg_id = ? AND DATE(started_at) = ?
        """, (user_id, today)) as cursor:
            sessions_count = (await cursor.fetchone())[0]
        
        if sessions_count >= 1:
            title = ux.h1("Лимит фокус-сессий", "⏰")
            intro = ux.p("Бесплатный план: 1 сессия 25 минут в день.")
            features = [
                "🎯 Неограниченные сессии",
                "⏱️ Сессии 25 и 45 минут",
                "📊 Расширенная статистика"
            ]
            body = ux.block("Pro возможности", features, "✨")
            footer = ux.p("Pro — 199 ₽/мес. 5 дней — бесплатно.")
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="Оформить Pro в Tribute", 
                    url=config.tribute_product_url
                )],
                [InlineKeyboardButton(text="↩️ В меню", callback_data="nav:menu")]
            ])
            
            if isinstance(event, Message):
                await event.answer(
                    ux.compose(title, intro, body, ux.hr(), footer),
                    reply_markup=keyboard
                )
            else:
                await event.message.edit_text(
                    ux.compose(title, intro, body, ux.hr(), footer),
                    reply_markup=keyboard
                )
                await event.answer()
            return
        
        # Лимит не превышен, разрешаем доступ
        return True
