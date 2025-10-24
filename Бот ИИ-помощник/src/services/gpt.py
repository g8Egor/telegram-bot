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
    
    async def build_profile(self, answers_10q: List[str]) -> Dict[str, Any]:
        """Строит психологический профиль на основе 10 вопросов."""
        prompt = f"""Ты - опытный психолог. Проанализируй ответы пользователя и создай психологический профиль.

Ответы пользователя:
1. {answers_10q[0] if len(answers_10q) > 0 else 'Не отвечен'}
2. {answers_10q[1] if len(answers_10q) > 1 else 'Не отвечен'}
3. {answers_10q[2] if len(answers_10q) > 2 else 'Не отвечен'}
4. {answers_10q[3] if len(answers_10q) > 3 else 'Не отвечен'}
5. {answers_10q[4] if len(answers_10q) > 4 else 'Не отвечен'}
6. {answers_10q[5] if len(answers_10q) > 5 else 'Не отвечен'}
7. {answers_10q[6] if len(answers_10q) > 6 else 'Не отвечен'}
8. {answers_10q[7] if len(answers_10q) > 7 else 'Не отвечен'}
9. {answers_10q[8] if len(answers_10q) > 8 else 'Не отвечен'}
10. {answers_10q[9] if len(answers_10q) > 9 else 'Не отвечен'}

Верни ТОЛЬКО JSON без дополнительного текста:
{{
  "personality_type": "тип личности",
  "detailed_analysis": "детальный анализ",
  "strengths": ["сила1", "сила2", "сила3"],
  "growth_areas": ["область1", "область2"],
  "communication_style": "стиль общения",
  "motivation_factors": ["фактор1", "фактор2"],
  "personal_advice": "персональный совет"
}}"""
        
        messages = [{"role": "user", "content": prompt}]
        response = await self._make_request(messages)
        
        try:
            import json
            import re
            
            # Очищаем ответ от лишних символов
            cleaned_response = response.strip()
            
            # Ищем JSON в тексте
            json_match = re.search(r'\{.*\}', cleaned_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                # Если JSON не найден, пытаемся парсить весь ответ
                return json.loads(cleaned_response)
                
        except (json.JSONDecodeError, AttributeError) as e:
            logger.error(f"Failed to parse profile JSON: {e}")
            logger.error(f"Response was: {response[:200]}...")
            
            # Возвращаем профиль на основе ответов пользователя
            return {
                "personality_type": "Адаптивная личность",
                "detailed_analysis": f"На основе ваших ответов: {', '.join(answers_10q[:3])} - вы демонстрируете уникальный подход к жизни. Ваши ответы показывают индивидуальность и способность к рефлексии.",
                "strengths": ["Самоанализ", "Целеустремленность", "Адаптивность", "Рефлексия"],
                "growth_areas": ["Эмоциональная гибкость", "Коммуникация", "Самопринятие"],
                "communication_style": "Искренний и открытый",
                "motivation_factors": ["Личностный рост", "Самореализация", "Развитие"],
                "personal_advice": "Продолжайте развивать самосознание и используйте свои сильные стороны для достижения целей. Не забывайте о важности баланса между амбициями и внутренним покоем."
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
