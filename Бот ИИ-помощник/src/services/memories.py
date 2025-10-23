"""Сервис для работы с памятью пользователя."""
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ..storage import db
from ..logger import get_logger

logger = get_logger("memories")


class MemoryService:
    """Сервис для управления памятью пользователя."""
    
    @staticmethod
    async def add_memory(tg_id: int, kind: str, content: str) -> None:
        """Добавляет запись в память."""
        await db.add_memory(tg_id, kind, content)
        logger.info(f"Added memory for user {tg_id}: {kind}")
    
    @staticmethod
    async def get_recent_memories(tg_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Получает последние записи памяти."""
        return await db.recent_memories(tg_id, limit)
    
    @staticmethod
    async def get_memories_by_type(tg_id: int, kind: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Получает записи памяти определенного типа."""
        # Это упрощенная версия - в реальности нужен отдельный метод в storage
        all_memories = await db.recent_memories(tg_id, limit * 2)
        return [m for m in all_memories if m['kind'] == kind][:limit]
    
    @staticmethod
    async def summarize_dialog(tg_id: int, dialog_content: str) -> str:
        """Создает краткое резюме диалога для сохранения в память."""
        # В реальной реализации здесь был бы вызов GPT для создания резюме
        # Пока возвращаем первые 200 символов
        return dialog_content[:200] + "..." if len(dialog_content) > 200 else dialog_content
    
    @staticmethod
    async def get_context_for_gpt(tg_id: int, context_types: List[str] = None) -> str:
        """Получает контекст для GPT на основе памяти."""
        if context_types is None:
            context_types = ['morning', 'evening', 'reflect']
        
        memories = await db.recent_memories(tg_id, 5)
        relevant_memories = [m for m in memories if m['kind'] in context_types]
        
        if not relevant_memories:
            return "Контекст отсутствует."
        
        context_parts = []
        for memory in relevant_memories:
            context_parts.append(f"[{memory['kind']}] {memory['content']}")
        
        return "\n".join(context_parts)
    
    @staticmethod
    async def cleanup_old_memories(tg_id: int, days_old: int = 30) -> int:
        """Очищает старые записи памяти (оставляем только последние N дней)."""
        # В реальной реализации нужен метод в storage для удаления старых записей
        # Пока возвращаем 0
        return 0


# Глобальный экземpляр сервиса
memory_service = MemoryService()
