"""Централизованное логирование."""
import logging
import sys
from datetime import datetime
from typing import Optional
import uuid


class RequestIDFilter(logging.Filter):
    """Фильтр для добавления request_id в логи."""
    
    def filter(self, record):
        if not hasattr(record, 'request_id'):
            record.request_id = str(uuid.uuid4())[:8]
        return True


def setup_logger(name: str = "personal_brain", level: str = "INFO") -> logging.Logger:
    """Настраивает логгер с ISO-временем и request_id."""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Удаляем существующие обработчики
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Создаем форматтер с ISO-временем
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(request_id)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(RequestIDFilter())
    logger.addHandler(console_handler)
    
    # Файловый обработчик
    file_handler = logging.FileHandler('bot.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestIDFilter())
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Получает логгер по имени."""
    if name:
        return logging.getLogger(f"personal_brain.{name}")
    return logging.getLogger("personal_brain")


def log_secret_safe(logger: logging.Logger, message: str, secret: str) -> None:
    """Логирует сообщение, скрывая секреты."""
    safe_secret = secret[:4] + "..." + secret[-4:] if len(secret) > 8 else "***"
    logger.info(f"{message}: {safe_secret}")


def log_user_action(logger: logging.Logger, user_id: int, action: str, details: str = "") -> None:
    """Логирует действия пользователя."""
    logger.info(f"User {user_id} | {action} | {details}")


def log_error_safe(logger: logging.Logger, error: Exception, context: str = "") -> None:
    """Безопасно логирует ошибки без чувствительных данных."""
    error_msg = f"Error in {context}: {type(error).__name__}: {str(error)}"
    logger.error(error_msg, exc_info=True)


# Глобальный логгер
logger = setup_logger()
