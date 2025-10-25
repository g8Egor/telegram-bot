"""Конфигурация приложения."""
import os
from typing import Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

load_dotenv()


class Config(BaseModel):
    """Основная конфигурация приложения."""
    
    # Telegram Bot
    bot_token: str = Field(..., description="Токен Telegram бота")
    admin_id: int = Field(..., description="ID администратора")
    
    # OpenAI
    openai_api_key: str = Field(..., description="Ключ OpenAI API")
    openai_model: str = Field(default="gpt-4o-mini", description="Модель OpenAI")
    
    # Timezone and Schedule
    default_tz: str = Field(default="Europe/Amsterdam", description="Часовой пояс по умолчанию")
    morning_hour: int = Field(default=8, ge=0, le=23, description="Час утреннего опроса")
    evening_hour: int = Field(default=20, ge=0, le=23, description="Час вечернего опроса")
    weekly_weekday: int = Field(default=6, ge=0, le=6, description="День недели для отчета (0=пн, 6=вс)")
    
    # Tribute Payments
    tribute_product_url: str = Field(default="https://t.me/tribute/app?startapp=plVY", description="Ссылка на продукт Tribute")
    tribute_webhook_secret: Optional[str] = Field(None, description="Секрет для подписи webhook Tribute")
    external_base_url: Optional[str] = Field(None, description="Публичный URL для webhook")
    
    # API Settings
    openai_timeout: int = Field(default=15, description="Таймаут OpenAI API в секундах")
    openai_retries: int = Field(default=3, description="Количество повторов для OpenAI API")
    http_timeout: int = Field(default=10, description="Таймаут HTTP запросов в секундах")
    
    # Rate Limiting
    cooldown_seconds: int = Field(default=5, description="Кудаун между командами в секундах")
    
    # Database
    db_path: str = Field(default="bot.db", description="Путь к файлу базы данных")
    
    @validator('bot_token', 'openai_api_key')
    def validate_required_secrets(cls, v):
        if not v:
            raise ValueError("Обязательный параметр не может быть пустым")
        return v
    
    @validator('morning_hour', 'evening_hour')
    def validate_hours(cls, v):
        if not 0 <= v <= 23:
            raise ValueError("Час должен быть от 0 до 23")
        return v
    
    @validator('weekly_weekday')
    def validate_weekday(cls, v):
        if not 0 <= v <= 6:
            raise ValueError("День недели должен быть от 0 до 6")
        return v


def load_config() -> Config:
    """Загружает конфигурацию из переменных окружения."""
    return Config(
        bot_token=os.getenv("BOT_TOKEN", ""),
        admin_id=int(os.getenv("ADMIN_ID", "0")),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        default_tz=os.getenv("DEFAULT_TZ", "Europe/Amsterdam"),
        morning_hour=int(os.getenv("MORNING_HOUR", "8")),
        evening_hour=int(os.getenv("EVENING_HOUR", "20")),
        weekly_weekday=int(os.getenv("WEEKLY_WEEKDAY", "6")),
        tribute_product_url=os.getenv("TRIBUTE_PRODUCT_URL", "https://t.me/tribute/app?startapp=plVY"),
        tribute_webhook_secret=os.getenv("TRIBUTE_WEBHOOK_SECRET"),
        external_base_url=os.getenv("EXTERNAL_BASE_URL"),
    )


# Глобальный экземпляр конфигурации
config = load_config()
