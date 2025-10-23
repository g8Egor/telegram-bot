"""Планировщик задач."""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from typing import Dict, Any

from .storage import db
from .services.gpt import gpt_service
from .services.memories import memory_service
from .services.reports import report_service
from .services.pdf import pdf_service
from .services.timeutils import time_utils
from .logger import get_logger

logger = get_logger("scheduler")


class SchedulerService:
    """Сервис планировщика задач."""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.active_jobs = {}  # Хранилище активных задач
    
    async def start(self):
        """Запускает планировщик."""
        self.scheduler.start()
        logger.info("Scheduler started")
    
    async def stop(self):
        """Останавливает планировщик."""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped")
    
    async def schedule_user_tasks(self, user_id: int):
        """Планирует задачи для конкретного пользователя."""
        user = await db.get_user(user_id)
        if not user:
            return
        
        # Удаляем существующие задачи пользователя
        await self.unschedule_user_tasks(user_id)
        
        # Планируем утренний опрос
        morning_time = time_utils.calculate_next_morning(user.tz, user.morning_hour)
        self.scheduler.add_job(
            self._send_morning_reminder,
            DateTrigger(run_date=morning_time),
            args=[user_id],
            id=f"morning_{user_id}",
            replace_existing=True
        )
        
        # Планируем вечерний опрос
        evening_time = time_utils.calculate_next_evening(user.tz, user.evening_hour)
        self.scheduler.add_job(
            self._send_evening_reminder,
            DateTrigger(run_date=evening_time),
            args=[user_id],
            id=f"evening_{user_id}",
            replace_existing=True
        )
        
        # Планируем еженедельный отчет
        weekly_time = time_utils.calculate_next_weekly_report(user.tz, 6, 18)
        self.scheduler.add_job(
            self._send_weekly_report,
            DateTrigger(run_date=weekly_time),
            args=[user_id],
            id=f"weekly_{user_id}",
            replace_existing=True
        )
        
        logger.info(f"Scheduled tasks for user {user_id}")
    
    async def unschedule_user_tasks(self, user_id: int):
        """Удаляет задачи пользователя."""
        job_ids = [f"morning_{user_id}", f"evening_{user_id}", f"weekly_{user_id}"]
        
        for job_id in job_ids:
            try:
                self.scheduler.remove_job(job_id)
            except Exception as e:
                logger.warning(f"Failed to remove job {job_id}: {e}")
        
        logger.info(f"Unscheduled tasks for user {user_id}")
    
    async def _send_morning_reminder(self, user_id: int):
        """Отправляет утреннее напоминание."""
        try:
            # Проверяем, не заполнен ли уже утренний опрос
            has_morning = await db.today_has(user_id, "morning")
            if has_morning:
                logger.info(f"Morning entry already exists for user {user_id}")
                return
            
            # Получаем бота из глобальной переменной
            try:
                from .main import bot
            except ImportError:
                # Если не можем импортировать, используем None
                bot = None
            
            if not bot:
                logger.error("Bot instance not available")
                return
            
            # Отправляем напоминание
            await bot.send_message(
                user_id,
                "🌅 Доброе утро! Время для планирования дня.\n\n"
                "Нажмите /start или используйте кнопку 'Мой день' для начала опроса."
            )
            
            logger.info(f"Morning reminder sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"Morning reminder error for user {user_id}: {e}")
    
    async def _send_evening_reminder(self, user_id: int):
        """Отправляет вечернее напоминание."""
        try:
            # Проверяем, не заполнен ли уже вечерний опрос
            has_evening = await db.today_has(user_id, "evening")
            if has_evening:
                logger.info(f"Evening entry already exists for user {user_id}")
                return
            
            # Получаем бота из глобальной переменной
            try:
                from .main import bot
            except ImportError:
                # Если не можем импортировать, используем None
                bot = None
            
            if not bot:
                logger.error("Bot instance not available")
                return
            
            # Отправляем напоминание
            await bot.send_message(
                user_id,
                "🌙 Добрый вечер! Время для рефлексии.\n\n"
                "Нажмите /start или используйте кнопку 'Мой день' для вечернего опроса."
            )
            
            logger.info(f"Evening reminder sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"Evening reminder error for user {user_id}: {e}")
    
    async def _send_weekly_report(self, user_id: int):
        """Отправляет еженедельный отчет."""
        try:
            user = await db.get_user(user_id)
            if not user:
                return
            
            # Генерируем отчет
            report = await report_service.generate_weekly_report(user_id, user.persona)
            
            # Получаем бота из глобальной переменной
            try:
                from .main import bot
            except ImportError:
                # Если не можем импортировать, используем None
                bot = None
            
            if not bot:
                logger.error("Bot instance not available")
                return
            
            # Отправляем отчет
            await bot.send_message(
                user_id,
                f"📊 Ваш еженедельный отчет:\n\n{report}"
            )
            
            # Если пользователь на Ultimate плане, генерируем PDF
            if user.plan_tier == "ultimate":
                try:
                    pdf_path = await pdf_service.generate_weekly_pdf(
                        user_id=user_id,
                        user_name=user.tz  # Используем tz как имя пользователя
                    )
                    
                    from aiogram.types import FSInputFile
                    pdf_file = FSInputFile(pdf_path)
                    
                    await bot.send_document(
                        user_id,
                        document=pdf_file,
                        caption="📄 PDF отчет за неделю"
                    )
                    
                except Exception as e:
                    logger.error(f"PDF generation error for user {user_id}: {e}")
            
            logger.info(f"Weekly report sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"Weekly report error for user {user_id}: {e}")
    
    async def schedule_habit_reminders(self, user_id: int, habit_name: str):
        """Планирует напоминания о привычках."""
        # В реальной реализации здесь была бы логика напоминаний о привычках
        # Пока это заглушка
        pass
    
    async def schedule_focus_reminders(self, user_id: int):
        """Планирует напоминания о фокус-сессиях."""
        # В реальной реализации здесь была бы логика напоминаний о фокус-сессиях
        # Пока это заглушка
        pass
    
    async def reschedule_all_users(self):
        """Перепланирует задачи для всех пользователей."""
        try:
            # Получаем всех пользователей
            async with db._connection.execute("SELECT tg_id FROM users") as cursor:
                users = await cursor.fetchall()
            
            for (user_id,) in users:
                await self.schedule_user_tasks(user_id)
            
            logger.info(f"Rescheduled tasks for {len(users)} users")
            
        except Exception as e:
            logger.error(f"Reschedule error: {e}")


# Глобальный экземпляр планировщика
scheduler_service = SchedulerService()
