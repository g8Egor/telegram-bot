"""Сервис для работы с платежами Tribute."""
import hashlib
import hmac
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import httpx

from ..config import config
from ..logger import get_logger

logger = get_logger("tribute")


class TributeService:
    """Сервис для работы с платежами Tribute."""
    
    def __init__(self):
        self.base_url = config.tribute_product_base_url
        self.webhook_secret = config.tribute_webhook_secret
        self.external_base_url = config.external_base_url
    
    async def build_buy_link(self, tg_id: int, plan_tier: str, period: str) -> str:
        """Строит ссылку на оплату в Tribute."""
        if not self.base_url:
            raise ValueError("TRIBUTE_PRODUCT_BASE_URL not configured")
        
        # Создаем external_id для отслеживания
        external_id = f"{tg_id}_{plan_tier}_{period}"
        
        # Параметры для ссылки
        params = {
            "external_id": external_id,
            "user_id": str(tg_id),
            "plan": plan_tier,
            "period": period,
            "return_url": f"{self.external_base_url}/tribute/success",
            "cancel_url": f"{self.external_base_url}/tribute/cancel"
        }
        
        # Строим URL с параметрами
        import urllib.parse
        query_string = urllib.parse.urlencode(params)
        payment_url = f"{self.base_url}?{query_string}"
        
        logger.info(f"Payment link generated for user {tg_id}: {plan_tier} {period}")
        return payment_url
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """Проверяет подпись webhook от Tribute."""
        if not self.webhook_secret:
            logger.warning("TRIBUTE_WEBHOOK_SECRET not configured")
            return False
        
        # Создаем ожидаемую подпись
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Сравниваем подписи
        return hmac.compare_digest(signature, expected_signature)
    
    def parse_webhook_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Парсит payload webhook от Tribute."""
        return {
            "external_id": payload.get("external_id"),
            "status": payload.get("status"),
            "amount": payload.get("amount"),
            "currency": payload.get("currency", "RUB"),
            "created_at": payload.get("created_at"),
            "user_id": payload.get("user_id"),
            "plan": payload.get("plan"),
            "period": payload.get("period")
        }
    
    async def process_payment(self, webhook_data: Dict[str, Any]) -> bool:
        """Обрабатывает успешный платеж."""
        try:
            external_id = webhook_data.get("external_id")
            if not external_id:
                logger.error("No external_id in webhook payload")
                return False
            
            # Парсим external_id
            parts = external_id.split("_")
            if len(parts) != 3:
                logger.error(f"Invalid external_id format: {external_id}")
                return False
            
            tg_id, plan_tier, period = int(parts[0]), parts[1], parts[2]
            
            # Определяем срок подписки
            if period == "monthly":
                expires_at = datetime.now() + timedelta(days=30)
            elif period == "yearly":
                expires_at = datetime.now() + timedelta(days=365)
            else:
                logger.error(f"Unknown period: {period}")
                return False
            
            # Обновляем подписку пользователя
            from ..storage import db
            await db.set_plan(tg_id, plan_tier, expires_at)
            
            # Логируем платеж
            await db._connection.execute("""
                INSERT INTO payments (tg_id, external_id, plan_tier, period, status, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tg_id, external_id, plan_tier, period, "paid", expires_at))
            await db._connection.commit()
            
            logger.info(f"Payment processed for user {tg_id}: {plan_tier} {period} until {expires_at}")
            return True
            
        except Exception as e:
            logger.error(f"Payment processing error: {e}")
            return False
    
    async def check_payment_status(self, external_id: str) -> Optional[Dict[str, Any]]:
        """Проверяет статус платежа по external_id."""
        try:
            # В реальной реализации здесь был бы запрос к API Tribute
            # Пока возвращаем None
            return None
        except Exception as e:
            logger.error(f"Payment status check error: {e}")
            return None
    
    async def get_user_payments(self, tg_id: int) -> list:
        """Получает историю платежей пользователя."""
        from ..storage import db
        
        async with db._connection.execute("""
            SELECT external_id, plan_tier, period, status, created_at, expires_at
            FROM payments 
            WHERE tg_id = ? 
            ORDER BY created_at DESC
        """, (tg_id,)) as cursor:
            rows = await cursor.fetchall()
            
            return [
                {
                    "external_id": row[0],
                    "plan_tier": row[1],
                    "period": row[2],
                    "status": row[3],
                    "created_at": row[4],
                    "expires_at": row[5]
                }
                for row in rows
            ]


# Глобальный экземпляр сервиса
tribute_service = TributeService()
