"""Сервис для генерации отчетов."""
from typing import Dict, Any, List
from datetime import datetime, timedelta, date
from ..storage import db
from ..services.gpt import gpt_service
from ..logger import get_logger

logger = get_logger("reports")


class ReportService:
    """Сервис для генерации отчетов."""
    
    @staticmethod
    async def generate_weekly_metrics(tg_id: int) -> Dict[str, Any]:
        """Генерирует метрики за неделю."""
        week_ago = (datetime.now() - timedelta(days=7)).date()
        
        # Базовые метрики из storage
        base_metrics = await db.week_stats(tg_id)
        
        # Дополнительные метрики
        # Количество привычек
        async with db._connection.execute("""
            SELECT COUNT(*) FROM habits WHERE tg_id = ?
        """, (tg_id,)) as cursor:
            habits_count = (await cursor.fetchone())[0]
        
        # Среднее настроение
        async with db._connection.execute("""
            SELECT AVG(mood) FROM mood 
            WHERE tg_id = ? AND date >= ?
        """, (tg_id, week_ago.isoformat())) as cursor:
            avg_mood = (await cursor.fetchone())[0] or 5
        
        # Количество дней с записями
        async with db._connection.execute("""
            SELECT COUNT(DISTINCT date) FROM entries 
            WHERE tg_id = ? AND date >= ?
        """, (tg_id, week_ago.isoformat())) as cursor:
            active_days = (await cursor.fetchone())[0]
        
        return {
            **base_metrics,
            "habits_count": habits_count,
            "avg_mood": round(avg_mood, 1),
            "active_days": active_days,
            "week_start": week_ago.isoformat(),
            "week_end": date.today().isoformat()
        }
    
    @staticmethod
    async def generate_weekly_report(tg_id: int, persona: str = "mentor") -> str:
        """Генерирует еженедельный отчет."""
        metrics = await ReportService.generate_weekly_metrics(tg_id)
        return await gpt_service.weekly_report(metrics, persona)
    
    @staticmethod
    async def get_habit_streaks(tg_id: int) -> List[Dict[str, Any]]:
        """Получает streak'и привычек."""
        async with db._connection.execute("""
            SELECT name, streak, last_tick FROM habits 
            WHERE tg_id = ? 
            ORDER BY streak DESC
        """, (tg_id,)) as cursor:
            rows = await cursor.fetchall()
            return [
                {
                    "name": row[0],
                    "streak": row[1],
                    "last_tick": row[2]
                }
                for row in rows
            ]
    
    @staticmethod
    async def get_focus_sessions(tg_id: int, days: int = 7) -> List[Dict[str, Any]]:
        """Получает сессии фокуса за период."""
        since = (datetime.now() - timedelta(days=days)).date()
        
        async with db._connection.execute("""
            SELECT started_at, duration, status FROM pomodoro 
            WHERE tg_id = ? AND DATE(started_at) >= ?
            ORDER BY started_at DESC
        """, (tg_id, since.isoformat())) as cursor:
            rows = await cursor.fetchall()
            return [
                {
                    "started_at": row[0],
                    "duration": row[1],
                    "status": row[2]
                }
                for row in rows
            ]
    
    @staticmethod
    async def get_mood_trend(tg_id: int, days: int = 7) -> List[Dict[str, Any]]:
        """Получает тренд настроения."""
        since = (datetime.now() - timedelta(days=days)).date()
        
        async with db._connection.execute("""
            SELECT date, energy, mood, note FROM mood 
            WHERE tg_id = ? AND date >= ?
            ORDER BY date ASC
        """, (tg_id, since.isoformat())) as cursor:
            rows = await cursor.fetchall()
            return [
                {
                    "date": row[0],
                    "energy": row[1],
                    "mood": row[2],
                    "note": row[3]
                }
                for row in rows
            ]
    
    @staticmethod
    async def get_productivity_score(tg_id: int) -> Dict[str, Any]:
        """Вычисляет общий балл продуктивности."""
        metrics = await ReportService.generate_weekly_metrics(tg_id)
        
        # Простая формула продуктивности
        score = 0
        
        # Активность (максимум 30 баллов)
        activity_score = min(30, metrics.get('active_days', 0) * 4.3)
        score += activity_score
        
        # Фокус (максимум 25 баллов)
        focus_score = min(25, metrics.get('focus_minutes', 0) / 4)
        score += focus_score
        
        # Энергия (максимум 25 баллов)
        energy_score = min(25, metrics.get('avg_energy', 5) * 2.5)
        score += energy_score
        
        # Привычки (максимум 20 баллов)
        habits_score = min(20, metrics.get('habits_count', 0) * 4)
        score += habits_score
        
        total_score = min(100, score)
        
        return {
            "total_score": round(total_score),
            "activity_score": round(activity_score),
            "focus_score": round(focus_score),
            "energy_score": round(energy_score),
            "habits_score": round(habits_score)
        }


# Глобальный экземпляр сервиса
report_service = ReportService()
