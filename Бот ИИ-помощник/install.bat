@echo off
echo 🔧 Установка зависимостей для бота 'Личный Мозг: Цифровое Я'...
echo.

echo 📦 Устанавливаю пакеты...
python -m pip install --upgrade pip
python -m pip install aiogram==3.22.0
python -m pip install apscheduler==3.11.0
python -m pip install aiosqlite==0.21.0
python -m pip install pydantic==2.11.10
python -m pip install python-dotenv==1.1.1
python -m pip install httpx==0.28.1
python -m pip install openai==2.6.0
python -m pip install fastapi==0.119.1
python -m pip install uvicorn==0.38.0
python -m pip install reportlab==4.4.4
python -m pip install pytz==2025.2

echo.
echo 🎉 Установка завершена!
echo 🚀 Теперь можно запустить бота: python main.py
pause
