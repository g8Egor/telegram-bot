"""Управление базой данных SQLite."""
import aiosqlite
import json
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass

from .config import config
from .logger import get_logger

logger = get_logger("storage")


@dataclass
class User:
    """Модель пользователя."""
    tg_id: int
    created_at: datetime
    plan_tier: str = "free"
    subscription_until: Optional[datetime] = None
    trial_until: Optional[datetime] = None
    tz: str = "Europe/Amsterdam"
    morning_hour: int = 8
    evening_hour: int = 20
    language: str = "ru"
    persona: str = "mentor"
    ref_code: Optional[str] = None
    ref_count: int = 0


class Database:
    """Класс для работы с базой данных."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.db_path
        self._connection: Optional[aiosqlite.Connection] = None
    
    async def connect(self):
        """Подключается к базе данных."""
        self._connection = await aiosqlite.connect(self.db_path)
        await self._create_tables()
        logger.info("Database connected")
    
    async def close(self):
        """Закрывает соединение с базой данных."""
        if self._connection:
            await self._connection.close()
            logger.info("Database disconnected")
    
    async def _create_tables(self):
        """Создает таблицы в базе данных."""
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                plan_tier TEXT DEFAULT 'free',
                subscription_until DATETIME,
                trial_until DATETIME,
                tz TEXT DEFAULT 'Europe/Amsterdam',
                morning_hour INTEGER DEFAULT 8,
                evening_hour INTEGER DEFAULT 20,
                language TEXT DEFAULT 'ru',
                persona TEXT DEFAULT 'mentor',
                ref_code TEXT,
                ref_count INTEGER DEFAULT 0
            )
        """):
            pass
        
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                tg_id INTEGER PRIMARY KEY,
                data JSON,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id)
            )
        """):
            pass
        
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                date TEXT,
                type TEXT CHECK(type IN ('morning','evening')),
                data JSON,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id)
            )
        """):
            pass
        
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                name TEXT,
                streak INTEGER DEFAULT 0,
                last_tick DATE,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id)
            )
        """):
            pass
        
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS pomodoro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                started_at DATETIME,
                finished_at DATETIME,
                duration INTEGER,
                status TEXT,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id)
            )
        """):
            pass
        
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS mood (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                date TEXT,
                energy INTEGER,
                mood INTEGER,
                note TEXT,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id)
            )
        """):
            pass
        
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                kind TEXT,
                content TEXT,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id)
            )
        """):
            pass
        
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                external_id TEXT,
                plan_tier TEXT,
                period TEXT,
                status TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id)
            )
        """):
            pass
        
        async with self._connection.execute("""
            CREATE TABLE IF NOT EXISTS abstinence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                name TEXT,
                start_date DATE,
                days_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tg_id) REFERENCES users (tg_id)
            )
        """):
            pass
        
        await self._connection.commit()
        logger.info("Database tables created/verified")
    
    # User management
    async def upsert_user(self, user: User) -> None:
        """Создает или обновляет пользователя."""
        await self._connection.execute("""
            INSERT OR REPLACE INTO users 
            (tg_id, created_at, plan_tier, subscription_until, trial_until, 
             tz, morning_hour, evening_hour, language, persona, ref_code, ref_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user.tg_id, user.created_at, user.plan_tier, user.subscription_until,
            user.trial_until, user.tz, user.morning_hour, user.evening_hour,
            user.language, user.persona, user.ref_code, user.ref_count
        ))
        await self._connection.commit()
    
    async def get_user(self, tg_id: int) -> Optional[User]:
        """Получает пользователя по ID."""
        async with self._connection.execute(
            "SELECT * FROM users WHERE tg_id = ?", (tg_id,)
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return User(
                    tg_id=row[0], created_at=datetime.fromisoformat(row[1]),
                    plan_tier=row[2], subscription_until=datetime.fromisoformat(row[3]) if row[3] else None,
                    trial_until=datetime.fromisoformat(row[4]) if row[4] else None,
                    tz=row[5], morning_hour=row[6], evening_hour=row[7],
                    language=row[8], persona=row[9], ref_code=row[10], ref_count=row[11]
                )
        return None
    
    async def set_plan(self, tg_id: int, plan_tier: str, expires_at: Optional[datetime] = None) -> None:
        """Устанавливает план пользователя."""
        await self._connection.execute(
            "UPDATE users SET plan_tier = ?, subscription_until = ? WHERE tg_id = ?",
            (plan_tier, expires_at, tg_id)
        )
        await self._connection.commit()
    
    async def is_pro(self, tg_id: int) -> bool:
        """Проверяет, есть ли у пользователя активная подписка."""
        user = await self.get_user(tg_id)
        if not user:
            return False
        
        if user.plan_tier == "free":
            return False
        
        if user.subscription_until and user.subscription_until > datetime.now():
            return True
        
        if user.trial_until and user.trial_until > datetime.now():
            return True
        
        return False
    
    # Entries
    async def save_entry(self, tg_id: int, entry_type: str, data: Dict[str, Any]) -> None:
        """Сохраняет запись утреннего/вечернего опроса."""
        today = date.today().isoformat()
        await self._connection.execute("""
            INSERT INTO entries (tg_id, date, type, data)
            VALUES (?, ?, ?, ?)
        """, (tg_id, today, entry_type, json.dumps(data)))
        await self._connection.commit()
    
    async def today_has(self, tg_id: int, entry_type: str) -> bool:
        """Проверяет, есть ли запись за сегодня."""
        today = date.today().isoformat()
        async with self._connection.execute("""
            SELECT COUNT(*) FROM entries 
            WHERE tg_id = ? AND date = ? AND type = ?
        """, (tg_id, today, entry_type)) as cursor:
            count = await cursor.fetchone()
            return count[0] > 0
    
    # Habits
    async def tick_habit(self, tg_id: int, habit_name: str) -> int:
        """Отмечает привычку и возвращает текущий streak."""
        today = date.today()
        
        # Получаем текущий streak
        async with self._connection.execute("""
            SELECT streak, last_tick FROM habits 
            WHERE tg_id = ? AND name = ?
        """, (tg_id, habit_name)) as cursor:
            row = await cursor.fetchone()
            
            if row:
                current_streak, last_tick = row[0], datetime.fromisoformat(row[1]).date() if row[1] else None
                
                # Если уже отмечали сегодня, не увеличиваем streak
                if last_tick == today:
                    return current_streak
                
                # Если вчера отмечали, увеличиваем streak
                if last_tick == today - timedelta(days=1):
                    new_streak = current_streak + 1
                else:
                    new_streak = 1
                
                await self._connection.execute("""
                    UPDATE habits SET streak = ?, last_tick = ? 
                    WHERE tg_id = ? AND name = ?
                """, (new_streak, today, tg_id, habit_name))
            else:
                new_streak = 1
                await self._connection.execute("""
                    INSERT INTO habits (tg_id, name, streak, last_tick)
                    VALUES (?, ?, ?, ?)
                """, (tg_id, habit_name, new_streak, today))
        
        await self._connection.commit()
        return new_streak
    
    # Pomodoro
    async def log_pomodoro(self, tg_id: int, started_at: datetime, finished_at: datetime, 
                          duration: int, status: str) -> None:
        """Логирует сессию помодоро."""
        await self._connection.execute("""
            INSERT INTO pomodoro (tg_id, started_at, finished_at, duration, status)
            VALUES (?, ?, ?, ?, ?)
        """, (tg_id, started_at, finished_at, duration, status))
        await self._connection.commit()
    
    # Mood
    async def save_mood(self, tg_id: int, energy: int, mood: int, note: str = "") -> None:
        """Сохраняет настроение."""
        today = date.today().isoformat()
        await self._connection.execute("""
            INSERT INTO mood (tg_id, date, energy, mood, note)
            VALUES (?, ?, ?, ?, ?)
        """, (tg_id, today, energy, mood, note))
        await self._connection.commit()
    
    # Memories
    async def add_memory(self, tg_id: int, kind: str, content: str) -> None:
        """Добавляет запись в память."""
        await self._connection.execute("""
            INSERT INTO memories (tg_id, kind, content)
            VALUES (?, ?, ?)
        """, (tg_id, kind, content))
        await self._connection.commit()
    
    async def recent_memories(self, tg_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Получает последние записи памяти."""
        async with self._connection.execute("""
            SELECT kind, content, ts FROM memories 
            WHERE tg_id = ? 
            ORDER BY ts DESC 
            LIMIT ?
        """, (tg_id, limit)) as cursor:
            rows = await cursor.fetchall()
            return [
                {"kind": row[0], "content": row[1], "ts": row[2]}
                for row in rows
            ]
    
    # Weekly stats
    async def week_stats(self, tg_id: int) -> Dict[str, Any]:
        """Получает статистику за неделю."""
        week_ago = (datetime.now() - timedelta(days=7)).date()
        
        # Количество записей
        async with self._connection.execute("""
            SELECT COUNT(*) FROM entries 
            WHERE tg_id = ? AND date >= ?
        """, (tg_id, week_ago.isoformat())) as cursor:
            entries_count = (await cursor.fetchone())[0]
        
        # Средняя энергия
        async with self._connection.execute("""
            SELECT AVG(energy) FROM mood 
            WHERE tg_id = ? AND date >= ?
        """, (tg_id, week_ago.isoformat())) as cursor:
            avg_energy = (await cursor.fetchone())[0] or 0
        
        # Активность по дням
        async with self._connection.execute("""
            SELECT date, COUNT(*) FROM entries 
            WHERE tg_id = ? AND date >= ?
            GROUP BY date
        """, (tg_id, week_ago.isoformat())) as cursor:
            daily_activity = dict(await cursor.fetchall())
        
        # Фокус-сессии
        async with self._connection.execute("""
            SELECT SUM(duration) FROM pomodoro 
            WHERE tg_id = ? AND started_at >= ?
        """, (tg_id, week_ago)) as cursor:
            focus_minutes = (await cursor.fetchone())[0] or 0
        
        return {
            "entries_count": entries_count,
            "avg_energy": round(avg_energy, 1),
            "daily_activity": daily_activity,
            "focus_minutes": focus_minutes
        }
    
    async def set_subscription_until(self, tg_id: int, until: datetime) -> None:
        """Устанавливает дату окончания подписки."""
        await self._connection.execute(
            "UPDATE users SET subscription_until = ? WHERE tg_id = ?",
            (until, tg_id)
        )
        await self._connection.commit()
    
    async def save_profile(self, tg_id: int, profile_data: str) -> None:
        """Сохраняет профиль пользователя."""
        await self._connection.execute("""
            INSERT OR REPLACE INTO profiles (tg_id, data, created_at)
            VALUES (?, ?, ?)
        """, (tg_id, profile_data, datetime.now()))
        await self._connection.commit()
    
    async def update_user_persona(self, tg_id: int, persona: str) -> None:
        """Обновляет персону пользователя."""
        await self._connection.execute(
            "UPDATE users SET persona = ? WHERE tg_id = ?",
            (persona, tg_id)
        )
        await self._connection.commit()


# Глобальный экземпляр базы данных
db = Database()
