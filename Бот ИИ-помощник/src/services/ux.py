"""Единый UX-форматтер для красивого отображения сообщений."""
from __future__ import annotations

EM = " "  # U+2003 EM SPACE для «красной строки»
SEP = "—" * 12

def h1(title: str, emoji: str = "🧠") -> str:
    return f"<b>{emoji} {escape(title)}</b>"

def h2(title: str, emoji: str = "✨") -> str:
    return f"<b>{emoji} {escape(title)}</b>"

def p(text: str) -> str:
    # абзац с «красной строкой»
    return f"{EM}{escape(text)}"

def ul(items: list[str], bullet: str = "•") -> str:
    lines = [f"{EM}{bullet} {escape(x)}" for x in items if x]
    return "\n".join(lines)

def code_inline(text: str) -> str:
    return f"<code>{escape(text)}</code>"

def hr() -> str:
    return f"<i>{SEP}</i>"

def block(title: str, items: list[str] | None = None, emoji: str = "📌", footer: str | None = None) -> str:
    parts = [h2(title, emoji)]
    if items:
        parts.append(ul(items))
    if footer:
        parts += [hr(), p(footer)]
    return "\n".join(parts)

def compose(*parts: str) -> str:
    return "\n\n".join([x for x in parts if x and x.strip()])

def escape(s: str) -> str:
    # HTML-escape для безопасного текста (минимальный)
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
