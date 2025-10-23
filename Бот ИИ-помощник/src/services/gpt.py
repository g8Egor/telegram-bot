"""Сервис для работы с OpenAI GPT."""
import asyncio
from typing import Dict, List, Any, Optional
import openai
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
    
    async def _make_request(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo") -> str:
        """Выполняет запрос к OpenAI с retry логикой."""
        for attempt in range(self.retries):
            try:
                response = await self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7,
                    timeout=self.timeout
                )
                return response.choices[0].message.content.strip()
            
            except Exception as e:
                logger.error(f"OpenAI request failed (attempt {attempt + 1}): {e}")
                if attempt == self.retries - 1:
                    # Если все попытки исчерпаны, возвращаем заглушку
                    return "Извините, временно не могу обработать запрос. Попробуйте позже."
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def build_profile(self, answers_10q: Dict[str, str]) -> Dict[str, Any]:
        """Строит психологический профиль на основе 10 вопросов."""
        prompt = f"""
        Ты - опытный психолог и коуч. Проанализируй ответы пользователя на 10 вопросов и создай детальный психологический профиль.
        
        Ответы пользователя:
        {answers_10q}
        
        Создай глубокий анализ личности, который будет:
        1. Детальным и конкретным (не общими фразами)
        2. Основанным на реальных ответах пользователя
        3. Практичным и полезным
        4. Красиво оформленным
        
        Верни JSON с полями:
        - personality_type: тип личности (конкретно, например "Амбициозный аналитик" или "Творческий интроверт")
        - detailed_analysis: развернутый анализ личности (2-3 абзаца, красиво написанный)
        - strengths: сильные стороны (4-6 конкретных пунктов)
        - growth_areas: области для развития (3-4 конкретных пункта)
        - communication_style: стиль общения (детально)
        - motivation_factors: факторы мотивации (конкретно)
        - personal_advice: персональный совет на основе анализа (1-2 абзаца, практичный)
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = await self._make_request(messages)
        
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error("Failed to parse profile JSON")
            return {
                "personality_type": "Аналитик",
                "detailed_analysis": "Вы демонстрируете аналитический подход к решению задач. Ваши ответы показывают системное мышление и стремление к структурированности. Это позволяет вам эффективно планировать и достигать поставленных целей.",
                "strengths": ["Целеустремленность", "Аналитическое мышление", "Системный подход", "Планирование"],
                "growth_areas": ["Эмоциональная гибкость", "Коммуникация", "Спонтанность"],
                "communication_style": "Прямой и конструктивный",
                "motivation_factors": ["Достижение целей", "Личностный рост", "Признание"],
                "personal_advice": "Используйте свой аналитический ум для планирования, но не забывайте о важности эмоционального интеллекта. Развивайте навыки общения и учитесь быть более гибким в неожиданных ситуациях."
            }
        except Exception as e:
            logger.error(f"Profile building failed: {e}")
            return {
                "personality_type": "Адаптивный",
                "detailed_analysis": "Вы обладаете высокой адаптивностью и способностью быстро приспосабливаться к изменениям. Ваши ответы показывают открытость новому опыту и готовность к развитию. Это ценные качества для современного мира.",
                "strengths": ["Гибкость", "Устойчивость", "Открытость", "Адаптивность"],
                "growth_areas": ["Технические навыки", "Коммуникация", "Фокус"],
                "communication_style": "Дружелюбный и открытый",
                "motivation_factors": ["Достижение целей", "Личностный рост", "Новые возможности"],
                "personal_advice": "Ваша адаптивность - это сила. Развивайте технические навыки и учитесь фокусироваться на долгосрочных целях, не теряя при этом гибкости в подходе."
            }
    
    async def plan_morning(self, goal: str, top3: List[str], energy: int, 
                          persona: str, memories: List[Dict[str, Any]]) -> str:
        """Планирует утро на основе целей и энергии."""
        memories_context = "\n".join([f"- {m['content']}" for m in memories[:3]])
        
        prompt = f"""
        Ты - {persona}. Помоги пользователю спланировать день.
        
        Цель дня: {goal}
        Топ-3 приоритета: {', '.join(top3)}
        Уровень энергии (1-10): {energy}
        
        Контекст из памяти:
        {memories_context}
        
        Дай краткий план дня (3-4 пункта) с учетом энергии и приоритетов.
        Будь практичным и мотивирующим.
        """
        
        messages = [{"role": "user", "content": prompt}]
        try:
            return await self._make_request(messages)
        except Exception as e:
            logger.error(f"GPT request failed: {e}")
            return "Извините, временно не могу обработать запрос. Попробуйте позже."
    
    async def reflect_evening(self, done: List[str], not_done: List[str], 
                             learning: str, persona: str, memories: List[Dict[str, Any]]) -> str:
        """Рефлексия вечером."""
        memories_context = "\n".join([f"- {m['content']}" for m in memories[:3]])
        
        prompt = f"""
        Ты - {persona}. Проведи вечернюю рефлексию.
        
        Выполнено: {', '.join(done)}
        Не выполнено: {', '.join(not_done)}
        Что узнал: {learning}
        
        Контекст:
        {memories_context}
        
        Дай краткую рефлексию (3-4 предложения) с выводами и советами на завтра.
        """
        
        messages = [{"role": "user", "content": prompt}]
        try:
            return await self._make_request(messages)
        except Exception as e:
            logger.error(f"GPT request failed: {e}")
            return "Извините, временно не могу обработать запрос. Попробуйте позже."
    
    async def reflect_dialog(self, user_prompt: str, profile: Dict[str, Any], 
                           persona: str, memories: List[Dict[str, Any]], 
                           mood_snapshot: Dict[str, int]) -> str:
        """Диалог с цифровым Я."""
        memories_context = "\n".join([f"- {m['content']}" for m in memories[:5]])
        
        prompt = f"""
        Ты - {persona}, персональный ассистент пользователя.
        
        Профиль пользователя:
        - Тип: {profile.get('personality_type', 'Не определен')}
        - Сильные стороны: {', '.join(profile.get('strengths', []))}
        - Области роста: {', '.join(profile.get('growth_areas', []))}
        
        Текущее состояние:
        - Энергия: {mood_snapshot.get('energy', 5)}/10
        - Настроение: {mood_snapshot.get('mood', 5)}/10
        
        Контекст из памяти:
        {memories_context}
        
        Вопрос пользователя: {user_prompt}
        
        Ответь как персональный ассистент, учитывая профиль и контекст.
        Будь поддерживающим и практичным.
        """
        
        messages = [{"role": "user", "content": prompt}]
        try:
            return await self._make_request(messages)
        except Exception as e:
            logger.error(f"GPT request failed: {e}")
            return "Извините, временно не могу обработать запрос. Попробуйте позже."
    
    async def weekly_report(self, metrics: Dict[str, Any], persona: str) -> str:
        """Генерирует еженедельный отчет."""
        prompt = f"""
        Ты - {persona}. Создай еженедельный отчет.
        
        Метрики:
        - Записей: {metrics.get('entries_count', 0)}
        - Средняя энергия: {metrics.get('avg_energy', 0)}/10
        - Фокус-сессии: {metrics.get('focus_minutes', 0)} минут
        - Активность по дням: {metrics.get('daily_activity', {})}
        
        Создай краткий отчет (5-6 предложений) с выводами и рекомендациями.
        """
        
        messages = [{"role": "user", "content": prompt}]
        try:
            return await self._make_request(messages)
        except Exception as e:
            logger.error(f"GPT request failed: {e}")
            return "Извините, временно не могу обработать запрос. Попробуйте позже."


# Глобальный экземпляр сервиса
gpt_service = GPTService()
