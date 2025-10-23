"""Утилиты для работы со временем."""
from datetime import datetime, time, timedelta
from typing import Optional
import pytz
from ..config import config
from ..logger import get_logger

logger = get_logger("timeutils")


class TimeUtils:
    """Утилиты для работы со временем."""
    
    @staticmethod
    def now_local(tz: str = None) -> datetime:
        """Получает текущее время в указанном часовом поясе."""
        if tz is None:
            tz = config.default_tz
        
        try:
            timezone = pytz.timezone(tz)
            return datetime.now(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            logger.warning(f"Unknown timezone: {tz}, using default")
            timezone = pytz.timezone(config.default_tz)
            return datetime.now(timezone)
    
    @staticmethod
    def get_user_timezone(user_tz: str) -> pytz.timezone:
        """Получает объект часового пояса пользователя."""
        try:
            return pytz.timezone(user_tz)
        except pytz.exceptions.UnknownTimeZoneError:
            logger.warning(f"Unknown user timezone: {user_tz}, using default")
            return pytz.timezone(config.default_tz)
    
    @staticmethod
    def calculate_next_morning(user_tz: str, morning_hour: int) -> datetime:
        """Вычисляет время следующего утреннего опроса."""
        timezone = TimeUtils.get_user_timezone(user_tz)
        now = datetime.now(timezone)
        
        # Время утреннего опроса сегодня
        today_morning = now.replace(hour=morning_hour, minute=0, second=0, microsecond=0)
        
        # Если уже прошло время утреннего опроса, планируем на завтра
        if now >= today_morning:
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=morning_hour, minute=0, second=0, microsecond=0)
        
        return today_morning
    
    @staticmethod
    def calculate_next_evening(user_tz: str, evening_hour: int) -> datetime:
        """Вычисляет время следующего вечернего опроса."""
        timezone = TimeUtils.get_user_timezone(user_tz)
        now = datetime.now(timezone)
        
        # Время вечернего опроса сегодня
        today_evening = now.replace(hour=evening_hour, minute=0, second=0, microsecond=0)
        
        # Если уже прошло время вечернего опроса, планируем на завтра
        if now >= today_evening:
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=evening_hour, minute=0, second=0, microsecond=0)
        
        return today_evening
    
    @staticmethod
    def calculate_next_weekly_report(user_tz: str, weekday: int, hour: int = 18) -> datetime:
        """Вычисляет время следующего еженедельного отчета."""
        timezone = TimeUtils.get_user_timezone(user_tz)
        now = datetime.now(timezone)
        
        # Находим следующий указанный день недели
        days_ahead = weekday - now.weekday()
        if days_ahead <= 0:  # Если день уже прошел на этой неделе
            days_ahead += 7
        
        next_report = now + timedelta(days=days_ahead)
        return next_report.replace(hour=hour, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def is_morning_time(user_tz: str, morning_hour: int, tolerance_minutes: int = 30) -> bool:
        """Проверяет, подходящее ли время для утреннего опроса."""
        timezone = TimeUtils.get_user_timezone(user_tz)
        now = datetime.now(timezone)
        
        morning_time = now.replace(hour=morning_hour, minute=0, second=0, microsecond=0)
        tolerance = timedelta(minutes=tolerance_minutes)
        
        return morning_time - tolerance <= now <= morning_time + tolerance
    
    @staticmethod
    def is_evening_time(user_tz: str, evening_hour: int, tolerance_minutes: int = 30) -> bool:
        """Проверяет, подходящее ли время для вечернего опроса."""
        timezone = TimeUtils.get_user_timezone(user_tz)
        now = datetime.now(timezone)
        
        evening_time = now.replace(hour=evening_hour, minute=0, second=0, microsecond=0)
        tolerance = timedelta(minutes=tolerance_minutes)
        
        return evening_time - tolerance <= now <= evening_time + tolerance
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%d.%m.%Y %H:%M") -> str:
        """Форматирует datetime в строку."""
        return dt.strftime(format_str)
    
    @staticmethod
    def get_week_start(user_tz: str) -> datetime:
        """Получает начало текущей недели (понедельник)."""
        timezone = TimeUtils.get_user_timezone(user_tz)
        now = datetime.now(timezone)
        
        # Находим понедельник этой недели
        days_since_monday = now.weekday()
        week_start = now - timedelta(days=days_since_monday)
        return week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def get_week_end(user_tz: str) -> datetime:
        """Получает конец текущей недели (воскресенье)."""
        week_start = TimeUtils.get_week_start(user_tz)
        return week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)


# Глобальный экземпляр утилит
time_utils = TimeUtils()
