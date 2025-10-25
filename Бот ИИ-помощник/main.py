"""Главный файл приложения."""
import asyncio
import signal
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from src.config import config
from src.logger import get_logger
from src.storage import db
from src.scheduler import scheduler_service
from src.middlewares.subscription_gate import SubscriptionGateMiddleware
from src.payments.tribute import tribute_service
from src.services.gpt import gpt_service

# Импорты обработчиков
from src.handlers import start, menu, morning, evening, focus, habits, mood, reflect, weekly, settings, billing, common, profile, abstinence

logger = get_logger("main")

# Глобальная переменная для бота
bot = None


async def periodic_alive_log():
    """Периодически логирует 'alive' для мониторинга."""
    while True:
        try:
            await asyncio.sleep(300)  # Каждые 5 минут
            logger.info("Bot alive - all systems operational")
        except Exception as e:
            logger.error(f"Periodic log error: {e}")
            await asyncio.sleep(60)  # При ошибке ждем минуту


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Запуск
    logger.info("Starting application...")
    
    try:
        # Подключаемся к базе данных
        await db.connect()
        logger.info("Database connected")
        
        # Проверяем OpenAI API
        await gpt_service.health_check()
        
        # Запускаем планировщик
        await scheduler_service.start()
        logger.info("Scheduler started")
        
        # Планируем задачи для всех пользователей
        await scheduler_service.reschedule_all_users()
        logger.info("User tasks scheduled")
        
        # Запускаем периодический лог "alive"
        asyncio.create_task(periodic_alive_log())
        
        logger.info("Application started successfully")
        yield
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    
    finally:
        # Остановка
        logger.info("Stopping application...")
        
        try:
            # Останавливаем планировщик
            await scheduler_service.stop()
            logger.info("Scheduler stopped")
            
            # Закрываем базу данных
            await db.close()
            logger.info("Database disconnected")
            
            logger.info("Application stopped")
            
        except Exception as e:
            logger.error(f"Shutdown error: {e}")


# Создаем FastAPI приложение
app = FastAPI(
    title="Personal Brain Bot",
    description="Telegram bot for personal development and productivity",
    version="1.0.0",
    lifespan=lifespan
)


async def setup_bot():
    """Настраивает и запускает Telegram бота."""
    global bot
    
    try:
        from aiogram import Bot, Dispatcher
        from aiogram.fsm.storage.memory import MemoryStorage
        
        # Создаем бота и диспетчер
        from aiogram.client.default import DefaultBotProperties
        bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
        dp = Dispatcher(storage=MemoryStorage())
        
        # Добавляем middleware
        dp.message.middleware(SubscriptionGateMiddleware())
        dp.callback_query.middleware(SubscriptionGateMiddleware())
        
        dp.include_router(start.router)
        dp.include_router(common.router)  # Общие обработчики (отмена) - первыми
        dp.include_router(profile.router)  # Профиль должен быть раньше меню
        dp.include_router(mood.router)  # Настроение должно быть раньше меню
        dp.include_router(menu.router)
        dp.include_router(morning.router)
        dp.include_router(evening.router)
        dp.include_router(focus.router)
        dp.include_router(habits.router)
        dp.include_router(reflect.router)
        dp.include_router(weekly.router)
        dp.include_router(abstinence.router)
        dp.include_router(settings.router)
        dp.include_router(billing.router)
        
        # Запускаем бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Bot setup error: {e}")
        raise


@app.post("/tribute/webhook")
async def tribute_webhook(request: Request):
    """Webhook для обработки платежей Tribute."""
    try:
        # Получаем заголовки
        signature = request.headers.get("X-Tribute-Signature", "")
        content_type = request.headers.get("Content-Type", "")
        
        # Получаем тело запроса
        body = await request.body()
        payload = body.decode('utf-8')
        
        # Проверяем подпись
        if not tribute_service.verify_webhook_signature(payload, signature):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Парсим payload
        import json
        webhook_data = json.loads(payload)
        parsed_data = tribute_service.parse_webhook_payload(webhook_data)
        
        # Обрабатываем платеж
        if parsed_data.get("status") == "paid":
            success = await tribute_service.process_payment(parsed_data)
            if success:
                logger.info(f"Payment processed: {parsed_data.get('external_id')}")
                return JSONResponse({"status": "success"})
            else:
                logger.error(f"Payment processing failed: {parsed_data.get('external_id')}")
                raise HTTPException(status_code=500, detail="Payment processing failed")
        
        return JSONResponse({"status": "ignored"})
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения."""
    try:
        # Проверяем доступность базы данных
        db_status = "ok" if db._connection else "error"
        
        # Проверяем доступность GPT
        gpt_status = "ok" if gpt_service.gpt_available else "offline"
        
        return {
            "status": "ok",
            "timestamp": str(asyncio.get_event_loop().time()),
            "database": db_status,
            "gpt": gpt_status,
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": str(asyncio.get_event_loop().time())
        }


@app.get("/")
async def root():
    """Корневой endpoint."""
    return {"message": "Personal Brain Bot API", "version": "1.0.0"}


async def graceful_shutdown():
    """Graceful shutdown приложения."""
    logger.info("Received shutdown signal")
    
    try:
        # Останавливаем планировщик
        await scheduler_service.stop()
        
        # Закрываем базу данных
        await db.close()
        
        logger.info("Graceful shutdown completed")
        
    except Exception as e:
        logger.error(f"Shutdown error: {e}")


def setup_signal_handlers():
    """Настраивает обработчики сигналов."""
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}")
        asyncio.create_task(graceful_shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Главная функция приложения."""
    try:
        # Настраиваем обработчики сигналов
        setup_signal_handlers()
        
        # Запускаем FastAPI сервер
        config_uvicorn = uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8001,
            log_level="info"
        )
        
        server = uvicorn.Server(config_uvicorn)
        
        # Запускаем сервер и бота параллельно
        await asyncio.gather(
            server.serve(),
            setup_bot()
        )
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Main error: {e}")
        sys.exit(1)
    finally:
        await graceful_shutdown()


if __name__ == "__main__":
    asyncio.run(main())