"""Сервис для анализа эмоций и настроения."""
import re
from typing import Dict, List, Any
from ..logger import get_logger

logger = get_logger("emotion")


class EmotionService:
    """Сервис для анализа эмоций в тексте."""
    
    # Эмоциональные слова и их веса
    POSITIVE_WORDS = {
        'отлично': 3, 'прекрасно': 3, 'замечательно': 3, 'великолепно': 3,
        'хорошо': 2, 'хороший': 2, 'отличный': 2, 'прекрасный': 2,
        'рад': 2, 'радость': 2, 'счастлив': 3, 'счастье': 3,
        'успех': 2, 'успешный': 2, 'достижение': 2, 'победа': 3,
        'люблю': 3, 'нравится': 2, 'приятно': 2, 'удовольствие': 2,
        'энергия': 2, 'энергичный': 2, 'активный': 2, 'мотивация': 2
    }
    
    NEGATIVE_WORDS = {
        'плохо': -2, 'плохой': -2, 'ужасно': -3, 'ужасный': -3,
        'грустно': -2, 'грустный': -2, 'печально': -2, 'печальный': -2,
        'устал': -2, 'усталость': -2, 'усталый': -2, 'изнеможение': -3,
        'стресс': -2, 'стрессовый': -2, 'напряжение': -2, 'тревога': -2,
        'злой': -2, 'злость': -2, 'раздражение': -2, 'фрустрация': -2,
        'беспокойство': -2, 'тревожный': -2, 'волнение': -2, 'паника': -3,
        'депрессия': -3, 'депрессивный': -3, 'апатия': -2, 'безразличие': -2
    }
    
    STRESS_INDICATORS = {
        'стресс': 3, 'напряжение': 3, 'давление': 3, 'перегрузка': 3,
        'тревога': 2, 'беспокойство': 2, 'волнение': 2, 'паника': 3,
        'дедлайн': 2, 'срочно': 2, 'быстро': 1, 'много': 1,
        'не успеваю': 3, 'не хватает': 2, 'слишком': 1
    }
    
    @classmethod
    def score_text(cls, text: str) -> Dict[str, Any]:
        """Анализирует эмоциональную окраску текста."""
        if not text:
            return {"polarity": 0, "stress": 0, "keywords": []}
        
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        polarity_score = 0
        stress_score = 0
        keywords = []
        
        # Анализ позитивных слов
        for word, weight in cls.POSITIVE_WORDS.items():
            if word in text_lower:
                polarity_score += weight
                keywords.append(f"+{word}")
        
        # Анализ негативных слов
        for word, weight in cls.NEGATIVE_WORDS.items():
            if word in text_lower:
                polarity_score += weight
                keywords.append(f"-{word}")
        
        # Анализ стресса
        for word, weight in cls.STRESS_INDICATORS.items():
            if word in text_lower:
                stress_score += weight
                keywords.append(f"!{word}")
        
        # Нормализация polarity (-5 до +5)
        polarity = max(-5, min(5, polarity_score))
        
        # Нормализация stress (0 до 10)
        stress = max(0, min(10, stress_score))
        
        return {
            "polarity": polarity,
            "stress": stress,
            "keywords": keywords[:10]  # Ограничиваем количество ключевых слов
        }
    
    @classmethod
    def analyze_mood_pattern(cls, mood_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Анализирует паттерны настроения."""
        if not mood_history:
            return {"trend": "stable", "average": 5, "volatility": 0}
        
        moods = [entry.get('mood', 5) for entry in mood_history]
        energies = [entry.get('energy', 5) for entry in mood_history]
        
        avg_mood = sum(moods) / len(moods)
        avg_energy = sum(energies) / len(energies)
        
        # Вычисляем тренд
        if len(moods) >= 3:
            recent_trend = sum(moods[-3:]) / 3 - sum(moods[:3]) / 3
            if recent_trend > 1:
                trend = "improving"
            elif recent_trend < -1:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        # Вычисляем волатильность
        volatility = max(moods) - min(moods) if len(moods) > 1 else 0
        
        return {
            "trend": trend,
            "average_mood": round(avg_mood, 1),
            "average_energy": round(avg_energy, 1),
            "volatility": volatility
        }
    
    @classmethod
    def get_mood_advice(cls, mood_data: Dict[str, Any]) -> str:
        """Получает совет на основе анализа настроения."""
        polarity = mood_data.get('polarity', 0)
        stress = mood_data.get('stress', 0)
        
        if polarity > 2 and stress < 3:
            return "Отличное настроение! Продолжайте в том же духе."
        elif polarity > 0 and stress < 5:
            return "Хорошее настроение. Попробуйте заняться чем-то новым."
        elif polarity < -2 or stress > 7:
            return "Сложный период. Рекомендуем отдых и простые задачи."
        elif stress > 5:
            return "Высокий уровень стресса. Попробуйте техники релаксации."
        else:
            return "Нейтральное состояние. Планируйте день с учетом приоритетов."


# Глобальный экземпляр сервиса
emotion_service = EmotionService()
