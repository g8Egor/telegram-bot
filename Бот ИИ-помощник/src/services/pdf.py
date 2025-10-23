"""Сервис для генерации PDF отчетов."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, Any, List
from datetime import datetime, date
import os

from ..services.reports import report_service
from ..logger import get_logger

logger = get_logger("pdf")


class PDFService:
    """Сервис для генерации PDF отчетов."""
    
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
    
    async def generate_weekly_pdf(self, tg_id: int, user_name: str = "Пользователь") -> str:
        """Генерирует PDF отчет за неделю."""
        filename = f"weekly_{tg_id}_{date.today().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Получаем данные для отчета
        metrics = await report_service.generate_weekly_metrics(tg_id)
        habits = await report_service.get_habit_streaks(tg_id)
        focus_sessions = await report_service.get_focus_sessions(tg_id)
        mood_trend = await report_service.get_mood_trend(tg_id)
        productivity = await report_service.get_productivity_score(tg_id)
        
        # Создаем PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Заголовок
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        story.append(Paragraph(f"Еженедельный отчет - {user_name}", title_style))
        story.append(Spacer(1, 20))
        
        # Общая статистика
        story.append(Paragraph("Общая статистика", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        stats_data = [
            ["Метрика", "Значение"],
            ["Активных дней", str(metrics.get('active_days', 0))],
            ["Средняя энергия", f"{metrics.get('avg_energy', 0)}/10"],
            ["Фокус-сессии", f"{metrics.get('focus_minutes', 0)} мин"],
            ["Привычки", str(metrics.get('habits_count', 0))],
            ["Балл продуктивности", f"{productivity.get('total_score', 0)}/100"]
        ]
        
        stats_table = Table(stats_data, colWidths=[2*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        # Привычки
        if habits:
            story.append(Paragraph("Привычки", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            habits_data = [["Привычка", "Streak", "Последний раз"]]
            for habit in habits[:5]:  # Показываем топ-5
                habits_data.append([
                    habit['name'],
                    str(habit['streak']),
                    habit['last_tick'] or "Никогда"
                ])
            
            habits_table = Table(habits_data, colWidths=[2*inch, 1*inch, 1.5*inch])
            habits_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(habits_table)
            story.append(Spacer(1, 20))
        
        # Тренд настроения
        if mood_trend:
            story.append(Paragraph("Тренд настроения", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            mood_data = [["Дата", "Энергия", "Настроение", "Заметка"]]
            for mood in mood_trend[-7:]:  # Последние 7 записей
                mood_data.append([
                    mood['date'],
                    str(mood['energy']),
                    str(mood['mood']),
                    mood['note'][:30] + "..." if len(mood['note']) > 30 else mood['note']
                ])
            
            mood_table = Table(mood_data, colWidths=[1*inch, 0.8*inch, 0.8*inch, 2*inch])
            mood_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(mood_table)
            story.append(Spacer(1, 20))
        
        # Рекомендации
        story.append(Paragraph("Рекомендации", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        recommendations = []
        if productivity['total_score'] < 50:
            recommendations.append("• Сосредоточьтесь на выполнении основных задач")
        if metrics.get('focus_minutes', 0) < 60:
            recommendations.append("• Увеличьте время фокус-сессий")
        if metrics.get('active_days', 0) < 5:
            recommendations.append("• Старайтесь быть активными каждый день")
        if not habits:
            recommendations.append("• Добавьте полезные привычки")
        
        if not recommendations:
            recommendations.append("• Отличная работа! Продолжайте в том же духе")
        
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))
        
        # Подпись
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Сгенерировано: {datetime.now().strftime('%d.%m.%Y %H:%M')}", footer_style))
        
        # Собираем PDF
        doc.build(story)
        logger.info(f"Generated PDF report: {filepath}")
        
        return filepath


# Глобальный экземпляр сервиса
pdf_service = PDFService()
