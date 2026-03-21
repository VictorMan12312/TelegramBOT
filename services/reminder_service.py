from typing import List, Tuple
from db import queries
from models.reminder import Reminder
from nlp.parser import parse_natural_language

class ReminderService:
    @staticmethod
    def add_reminder(user_id: int, text: str) -> str:
        if not text:
            return "El texto del recordatorio no puede estar vacío."
        
        parsed = parse_natural_language(text)
        due_date = parsed["datetime"]
        
        reminder = Reminder(
            id=None,
            user_id=user_id,
            title=parsed["title"],
            status='pending',
            due_date=due_date
        )
        
        try:
            reminder_id = queries.create_reminder(reminder)
            return f"Recordatorio creado con ID: {reminder_id}"
        except Exception as e:
            return f"Error al crear el recordatorio: {e}"

    @staticmethod
    def get_user_reminders(user_id: int) -> Tuple[bool, str | List[Reminder]]:
        try:
            reminders = queries.get_reminders_by_user(user_id)
            if not reminders:
                return False, "No tienes recordatorios."
            return True, reminders
        except Exception as e:
            return False, f"Error al obtener recordatorios: {e}"

    @staticmethod
    def update_reminder(user_id: int, reminder_id_str: str, new_text: str) -> str:
        if not reminder_id_str.isdigit():
            return "El ID del recordatorio debe ser numérico."
        if not new_text:
            return "El nuevo texto no puede estar vacío."
            
        reminder_id = int(reminder_id_str)
        try:
            success = queries.update_reminder_title(reminder_id, user_id, new_text.strip())
            if success:
                return f"Recordatorio {reminder_id} actualizado exitosamente."
            return f"No se encontró el recordatorio {reminder_id} o no te pertenece."
        except Exception as e:
            return f"Error al actualizar el recordatorio: {e}"

    @staticmethod
    def delete_reminder(user_id: int, reminder_id_str: str) -> str:
        if not reminder_id_str.isdigit():
            return "El ID del recordatorio debe ser numérico."
            
        reminder_id = int(reminder_id_str)
        try:
            success = queries.delete_reminder(reminder_id, user_id)
            if success:
                return f"Recordatorio {reminder_id} eliminado exitosamente."
            return f"No se encontró el recordatorio {reminder_id} o no te pertenece."
        except Exception as e:
            return f"Error al eliminar el recordatorio: {e}"

    @staticmethod
    def mark_as_done(user_id: int, reminder_id_str: str) -> str:
        if not reminder_id_str.isdigit():
            return "El ID del recordatorio debe ser numérico."
            
        reminder_id = int(reminder_id_str)
        try:
            success = queries.update_reminder_status(reminder_id, user_id, 'done')
            if success:
                return f"Recordatorio {reminder_id} marcado como completado."
            return f"No se encontró el recordatorio {reminder_id} o no te pertenece."
        except Exception as e:
            return f"Error al completar el recordatorio: {e}"
