"""Утилиты для финализации потоков (единый UX)."""
from __future__ import annotations
from aiogram.types import Message
from . import ux


def finish_card(title: str, intro: str | None = None, tips: list[str] | None = None, footer: str | None = None) -> str:
    """Создает финальную карточку для завершения потока."""
    parts = [ux.h1(title, "✅")]
    if intro:
        parts.append(ux.p(intro))
    if tips:
        parts.append(ux.block("Что дальше", tips, "➡️"))
    if footer:
        parts += [ux.hr(), ux.p(footer)]
    return ux.compose(*parts)
