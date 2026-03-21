from typing import List
from models.reminder import Reminder

def format_reminders_list(reminders: List[Reminder]) -> str:
    """Formatea la lista de recordatorios en un texto legible para el usuario."""
    if not reminders:
        return "No tienes recordatorios en este momento."
        
    lines = ["*Tus Recordatorios:*", ""]
    for r in reminders:
        estado = "[Completado]" if r.status == 'done' else "[Pendiente]"
        lines.append(f"{estado} *ID:* {r.position} - {r.title}")
        if r.due_date:
            lines.append(f"   Vence: {r.due_date.strftime('%Y-%m-%d %H:%M')}")
    
    return "\n".join(lines)
