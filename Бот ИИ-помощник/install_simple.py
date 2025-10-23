"""Простой установщик зависимостей."""
import subprocess
import sys

def install_packages():
    """Устанавливает все необходимые пакеты."""
    packages = [
        'aiogram==3.22.0',
        'apscheduler==3.11.0', 
        'aiosqlite==0.21.0',
        'pydantic==2.11.10',
        'python-dotenv==1.1.1',
        'httpx==0.28.1',
        'openai==2.6.0',
        'fastapi==0.119.1',
        'uvicorn==0.38.0',
        'reportlab==4.4.4',
        'pytz==2025.2'
    ]
    
    print("🔧 Установка зависимостей...")
    
    for package in packages:
        print(f"⏳ Устанавливаю {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} установлен")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка установки {package}: {e}")
            return False
    
    print("\n🎉 Все зависимости установлены!")
    return True

if __name__ == "__main__":
    success = install_packages()
    if success:
        print("\n🚀 Теперь можно запустить бота: python main.py")
    else:
        print("\n❌ Ошибка установки зависимостей")
    input("Нажмите Enter для выхода...")
