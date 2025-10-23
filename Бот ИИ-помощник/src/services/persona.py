"""Сервис для работы с персонами/ролями."""
from typing import Dict, List


class PersonaService:
    """Сервис для управления персонами."""
    
    PERSONAS = {
        "mentor": {
            "name": "Ментор",
            "description": "Мудрый наставник, который дает советы и направляет",
            "style": "Поддерживающий, мудрый, с акцентом на личностный рост и развитие"
        },
        "coach": {
            "name": "Коуч",
            "description": "Мотивирующий тренер, который помогает достигать целей",
            "style": "Энергичный, мотивирующий, с фокусом на результат и достижения"
        },
        "friend": {
            "name": "Друг",
            "description": "Понимающий друг, который всегда поддержит",
            "style": "Теплый, эмпатичный, с акцентом на эмоциональную поддержку"
        },
        "analyst": {
            "name": "Аналитик",
            "description": "Логичный аналитик, который помогает разобраться в данных",
            "style": "Логичный, структурированный, с фокусом на анализ и оптимизацию"
        }
    }
    
    @classmethod
    def get_persona(cls, persona_key: str) -> Dict[str, str]:
        """Получает информацию о персоне."""
        return cls.PERSONAS.get(persona_key, cls.PERSONAS["mentor"])
    
    @classmethod
    def get_all_personas(cls) -> Dict[str, Dict[str, str]]:
        """Получает все доступные персоны."""
        return cls.PERSONAS
    
    @classmethod
    def get_persona_list(cls) -> List[Dict[str, str]]:
        """Получает список персон для выбора."""
        return [
            {"key": key, **info}
            for key, info in cls.PERSONAS.items()
        ]
    
    @classmethod
    def get_system_prompt(cls, persona_key: str) -> str:
        """Получает системный промпт для персоны."""
        persona = cls.get_persona(persona_key)
        return f"""
        Ты - {persona['name']}. {persona['description']}
        
        Стиль общения: {persona['style']}
        
        Отвечай кратко, практично и по делу. Учитывай контекст пользователя и его цели.
        """
