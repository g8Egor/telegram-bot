"""Middleware для проверки подписки."""
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

from ..storage import db
from ..texts import texts
from ..logger import get_logger

logger = get_logger("subscription_gate")


class SubscriptionGateMiddleware(BaseMiddleware):
    """Middleware для проверки подписки пользователя."""
    
    def __init__(self):
        # Команды, доступные только с подпиской
        self.premium_commands = {
            texts.BUTTON_REFLECT,  # Mentor+
            "/export_pdf",        # Ultimate+
            "/check_payment"
        }
        
        # Команды с ограничениями для Free плана
        self.limited_commands = {
            texts.BUTTON_HABITS,  # Ограничение на количество привычек
            texts.BUTTON_FOCUS    # Ограничение на количество сессий
        }
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Проверяет подписку перед обработкой сообщения."""
        
        # Получаем ID пользователя
        if isinstance(event, Message):
            user_id = event.from_user.id
            text = event.text
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            text = event.data
        else:
            return await handler(event, data)
        
        # Проверяем, нужна ли подписка для этой команды
        if text in self.premium_commands:
            user = await db.get_user(user_id)
            if not user:
                await event.answer(texts.ERROR_NOT_FOUND)
                return
            
            # Проверяем пробный период
            from datetime import datetime
            if user.trial_until and user.trial_until > datetime.now():
                # Пробный период активен - разрешаем доступ
                pass
            elif user.plan_tier in ["pro", "mentor", "ult"] and user.subscription_until and user.subscription_until > datetime.now():
                # Активная подписка - проверяем уровень доступа
                if text == texts.BUTTON_REFLECT and user.plan_tier not in ["mentor", "ult"]:
                    await event.answer("❌ Диалог 'Цифровое Я' доступен только в тарифах Mentor и Ultimate")
                    return
                elif text == "/export_pdf" and user.plan_tier != "ult":
                    await event.answer("❌ PDF-отчёты доступны только в тарифе Ultimate")
                    return
            else:
                await event.answer(texts.PAYWALL)
                return
        
        # Проверяем ограничения для Free плана
        elif text in self.limited_commands:
            user = await db.get_user(user_id)
            if user:
                # Проверяем пробный период для всех пользователей
                from datetime import datetime
                if user.trial_until and user.trial_until > datetime.now():
                    # Пробный период активен - разрешаем без ограничений
                    return await handler(event, data)
                
                # Если не пробный период и план free - применяем ограничения
                if user.plan_tier == "free":
                    if text == texts.BUTTON_HABITS:
                        # Проверяем лимит привычек
                        async with db._connection.execute("""
                            SELECT COUNT(*) FROM habits WHERE tg_id = ?
                        """, (user_id,)) as cursor:
                            habits_count = (await cursor.fetchone())[0]
                        
                        if habits_count >= 2:
                            await event.answer(
                                "❌ Лимит привычек для Free плана: 2\n\n"
                                "Обновите подписку для неограниченного количества привычек.",
                                reply_markup=None
                            )
                            return
                    
                    elif text == texts.BUTTON_FOCUS:
                        # Проверяем лимит фокус-сессий
                        from datetime import date
                        today = date.today().isoformat()
                        
                        async with db._connection.execute("""
                            SELECT COUNT(*) FROM pomodoro 
                            WHERE tg_id = ? AND DATE(started_at) = ?
                        """, (user_id, today)) as cursor:
                            sessions_count = (await cursor.fetchone())[0]
                        
                        if sessions_count >= 1:
                            await event.answer(
                                "❌ Лимит фокус-сессий для Free плана: 1 в день\n\n"
                                "Обновите подписку для неограниченного количества сессий.",
                                reply_markup=None
                            )
                            return
        
        # Если все проверки пройдены, продолжаем обработку
        return await handler(event, data)
