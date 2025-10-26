"""Сервис для работы с OpenAI GPT."""
import asyncio
import json
import re
import uuid
import hashlib
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI
import httpx

from ..config import config
from ..logger import get_logger

logger = get_logger("gpt")


class GPTService:
    """Сервис для работы с OpenAI API."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.timeout = config.openai_timeout
        self.retries = config.openai_retries
        self.model = config.openai_model
        self.gpt_available = True
        self.last_response_hash = None
        
    async def health_check(self) -> bool:
        """Проверяет доступность OpenAI API."""
        try:
            import time
            start_time = time.time()
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10,
                timeout=5
            )
            latency = int((time.time() - start_time) * 1000)
            logger.info(f"OpenAI OK: {self.model}, {latency}ms")
            self.gpt_available = True
            return True
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            self.gpt_available = False
            return False
    
    async def _make_request(self, messages: List[Dict[str, str]], 
                          temperature: float = 0.7, 
                          max_tokens: int = 500) -> str:
        """Выполняет запрос к OpenAI с retry логикой."""
        if not self.gpt_available:
            return "ИИ временно недоступен. Попробуйте позже."
            
        request_id = str(uuid.uuid4())[:8]
        logger.info(f"GPT request {request_id}: {len(messages)} messages")
        
        for attempt in range(self.retries):
            try:
                import time
                start_time = time.time()
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=0.9,
                    timeout=self.timeout
                )
                
                latency = int((time.time() - start_time) * 1000)
                content = response.choices[0].message.content.strip()
                
                # Дедупликация ответов
                response_hash = hashlib.md5(content[-100:].encode()).hexdigest()
                if response_hash == self.last_response_hash and attempt < self.retries - 1:
                    logger.info(f"Duplicate response detected, retrying with jitter")
                    temperature += 0.1
                    await asyncio.sleep(1)
                    continue
                
                self.last_response_hash = response_hash
                logger.info(f"GPT response {request_id}: {latency}ms, {len(content)} chars")
                return content
            
            except Exception as e:
                logger.error(f"OpenAI request {request_id} failed (attempt {attempt + 1}): {e}")
                if attempt == self.retries - 1:
                    self.gpt_available = False
                    return "ИИ временно недоступен. Попробуйте позже."
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def build_profile(self, answers_10q: List[str]) -> Dict[str, Any]:
        """Строит психологический профиль на основе 10 вопросов."""
        if not self.gpt_available:
            return self._get_fallback_profile(answers_10q)
            
        # Структурируем ответы пользователя
        user_context = self._analyze_user_answers(answers_10q)
        
        prompt = f"""Ты - опытный психолог. Проанализируй ответы пользователя и создай персональный профиль.

Контекст пользователя:
{user_context}

Ответы на 10 вопросов:
{self._format_answers(answers_10q)}

Создай уникальный профиль на основе этих конкретных ответов. Верни ТОЛЬКО JSON:
{{
  "personality_type": "конкретный тип личности",
  "detailed_analysis": "детальный анализ на основе ответов",
  "strengths": ["сила1", "сила2", "сила3"],
  "growth_areas": ["область1", "область2"],
  "communication_style": "стиль общения",
  "motivation_factors": ["фактор1", "фактор2"],
  "personal_advice": "персональный совет"
}}"""
        
        messages = [{"role": "user", "content": prompt}]
        response = await self._make_request(messages, temperature=0.8)
        
        try:
            return self._parse_json_response(response)
        except Exception as e:
            logger.error(f"Profile parsing failed: {e}")
            return self._get_fallback_profile(answers_10q)
    
    def _analyze_user_answers(self, answers: List[str]) -> str:
        """Анализирует ответы пользователя для контекста."""
        if not answers or all(not a.strip() for a in answers):
            return "Недостаточно данных для анализа"
            
        # Простой анализ паттернов
        patterns = []
        if any("утром" in a.lower() or "рано" in a.lower() for a in answers):
            patterns.append("утренний тип")
        if any("вечером" in a.lower() or "поздно" in a.lower() for a in answers):
            patterns.append("вечерний тип")
        if any("спорт" in a.lower() or "тренировка" in a.lower() for a in answers):
            patterns.append("активный образ жизни")
        if any("книга" in a.lower() or "чтение" in a.lower() for a in answers):
            patterns.append("интеллектуальные интересы")
            
        return f"Паттерны: {', '.join(patterns) if patterns else 'уникальный подход'}"
    
    def _format_answers(self, answers: List[str]) -> str:
        """Форматирует ответы для промпта."""
        formatted = []
        for i, answer in enumerate(answers[:10], 1):
            if answer and answer.strip():
                formatted.append(f"{i}. {answer.strip()}")
            else:
                formatted.append(f"{i}. Не отвечен")
        return "\n".join(formatted)
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Парсит JSON ответ от GPT."""
        try:
            # Очищаем ответ
            cleaned = response.strip()
            
            # Ищем JSON в тексте
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                return json.loads(cleaned)
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"JSON parsing failed: {e}")
            raise
    
    def _get_fallback_profile(self, answers: List[str]) -> Dict[str, Any]:
        """Возвращает fallback профиль на основе ответов."""
        if not answers or all(not a.strip() for a in answers):
            return {
                "personality_type": "Исследователь",
                "detailed_analysis": "Пока недостаточно данных для глубокого анализа. Продолжайте использовать бота, и профиль станет более точным.",
                "strengths": ["Открытость к новому", "Готовность к развитию"],
                "growth_areas": ["Самопознание", "Рефлексия"],
                "communication_style": "Искренний",
                "motivation_factors": ["Личностный рост"],
                "personal_advice": "Продолжайте исследовать себя через ежедневные практики в боте."
            }
        
        # Анализируем ответы для персонализации
        unique_answers = [a for a in answers if a and a.strip()]
        context = f"На основе ваших ответов: {', '.join(unique_answers[:3])}"
        
        return {
            "personality_type": "Уникальная личность",
            "detailed_analysis": f"{context} - вы демонстрируете индивидуальный подход к жизни и готовность к саморазвитию.",
            "strengths": ["Самоанализ", "Целеустремленность", "Рефлексия"],
            "growth_areas": ["Эмоциональная гибкость", "Коммуникация"],
            "communication_style": "Искренний и открытый",
            "motivation_factors": ["Личностный рост", "Самореализация"],
            "personal_advice": "Используйте свои сильные стороны для достижения целей. Развивайте эмоциональный интеллект и коммуникативные навыки."
        }
    
    async def reflect_dialog(self, user_prompt: str, profile: Dict[str, Any], 
                           persona: str, memories: List[Dict[str, Any]], 
                           mood_snapshot: Dict[str, int]) -> str:
        """Диалог с цифровым Я."""
        if not self.gpt_available:
            return "ИИ временно недоступен. Попробуйте позже."
            
        memories_context = "\n".join([f"- {m['content']}" for m in memories[:5]])
        
        prompt = f"""Ты - {persona}, персональный ассистент.

Профиль пользователя:
- Тип: {profile.get('personality_type', 'Не определен')}
- Сильные стороны: {', '.join(profile.get('strengths', []))}
- Области роста: {', '.join(profile.get('growth_areas', []))}

Текущее состояние:
- Энергия: {mood_snapshot.get('energy', 5)}/10
- Настроение: {mood_snapshot.get('mood', 5)}/10

Контекст из памяти:
{memories_context}

Вопрос: {user_prompt}

Ответь как персональный ассистент в стиле {persona}. 
Дай 1 конкретный следующий шаг. Будь поддерживающим и практичным.
Максимум 2-6 строк."""
        
        messages = [{"role": "user", "content": prompt}]
        return await self._make_request(messages, temperature=0.7, max_tokens=200)
    
    async def plan_morning(self, goal: str, top3: List[str], energy: int, 
                          persona: str, memories: List[Dict[str, Any]]) -> str:
        """Планирует утро на основе целей и энергии."""
        if not self.gpt_available:
            return "ИИ временно недоступен. Попробуйте позже."
            
        memories_context = "\n".join([f"- {m['content']}" for m in memories[:3]])
        
        prompt = f"""Ты - {persona}. Помоги спланировать день.

Цель дня: {goal}
Топ-3 приоритета: {', '.join(top3)}
Уровень энергии (1-10): {energy}

Контекст: {memories_context}

Дай краткий план дня (3-4 пункта) с учетом энергии и приоритетов.
Будь практичным и мотивирующим."""
        
        messages = [{"role": "user", "content": prompt}]
        return await self._make_request(messages, temperature=0.7)
    
    async def reflect_evening(self, done: List[str], not_done: List[str], 
                             learning: str, persona: str, memories: List[Dict[str, Any]]) -> str:
        """Рефлексия вечером."""
        if not self.gpt_available:
            return "ИИ временно недоступен. Попробуйте позже."
            
        memories_context = "\n".join([f"- {m['content']}" for m in memories[:3]])
        
        prompt = f"""Ты - {persona}. Проведи вечернюю рефлексию.

Выполнено: {', '.join(done)}
Не выполнено: {', '.join(not_done)}
Что узнал: {learning}

Контекст: {memories_context}

Дай краткую рефлексию (3-4 предложения) с выводами и советами на завтра."""
        
        messages = [{"role": "user", "content": prompt}]
        return await self._make_request(messages, temperature=0.7)
    
    async def weekly_report(self, metrics: Dict[str, Any], persona: str) -> str:
        """Генерирует еженедельный отчет."""
        if not self.gpt_available:
            return "ИИ временно недоступен. Попробуйте позже."
            
        prompt = f"""Ты - {persona}. Создай еженедельный отчет.

Метрики:
- Записей: {metrics.get('entries_count', 0)}
- Средняя энергия: {metrics.get('avg_energy', 0)}/10
- Фокус-сессии: {metrics.get('focus_minutes', 0)} минут
- Активность: {metrics.get('daily_activity', {})}

Создай краткий отчет (5-6 предложений) с выводами и рекомендациями."""
        
        messages = [{"role": "user", "content": prompt}]
        return await self._make_request(messages, temperature=0.7)


# Глобальный экземпляр сервиса
gpt_service = GPTService()