from typing import List, Tuple
from db.repository import ReminderRepository
from models.reminder import Reminder
from nlp.parser import parse_natural_language
from core.sheduler import schedule_reminder

class ReminderService:
    """Clase que maneja toda la lógica de negocio de los recordatorios."""
    def __init__(self, job_queue, repo: ReminderRepository):
        self.job_queue = job_queue
        self.repo = repo

    def add_reminder(self, user_id: int, chat_id: int, text: str):
        """Crea un recordatorio extrayendo la fecha y el texto, y lo programa."""
        if not text:
            return {"success": False, "error": "Texto vacío"}

        parsed = parse_natural_language(text)
        title = parsed["title"]
        due_date = parsed["datetime"]

        reminder = Reminder(
            id=None,
            user_id=user_id,
            title=title,
            status="pending",
            due_date=due_date
        )

        self.repo.create_reminder(reminder)

        schedule_reminder(
            self.job_queue,
            user_id,
            chat_id,
            title,
            due_date
        )

        return {
            "success": True,
            "data": {
                "title": title,
                "due_date": due_date
            }
        }

    def get_user_reminders(self, user_id: int) -> Tuple[bool, str | List[Reminder]]:
        """Recupera la lista de recordatorios para un usuario específico."""
        try:
            reminders = self.repo.get_reminders_by_user(user_id)
            if not reminders:
                return False, "No tienes recordatorios."
            return True, reminders
        except Exception as e:
            return False, f"Error al obtener recordatorios: {e}"

    def update_reminder(self, user_id: int, reminder_id_str: str, new_text: str) -> str:
        """Actualiza el texto de un recordatorio si el usuario es dueño del mismo."""
        if not reminder_id_str.isdigit():
            return "El ID del recordatorio debe ser numérico."
        if not new_text:
            return "El nuevo texto no puede estar vacío."
            
        reminder_id = int(reminder_id_str)
        try:
            success = self.repo.update_reminder_title(reminder_id, user_id, new_text.strip())
            if success:
                return f"Recordatorio {reminder_id} actualizado exitosamente."
            return f"No se encontró el recordatorio {reminder_id} o no te pertenece."
        except Exception as e:
            return f"Error al actualizar el recordatorio: {e}"

    def delete_reminder(self, user_id: int, reminder_id_str: str) -> str:
        """Elimina permanentemente un recordatorio del usuario."""
        if not reminder_id_str.isdigit():
            return "El ID del recordatorio debe ser numérico."
            
        reminder_id = int(reminder_id_str)
        try:
            success = self.repo.delete_reminder(reminder_id, user_id)
            if success:
                return f"Recordatorio {reminder_id} eliminado exitosamente."
            return f"No se encontró el recordatorio {reminder_id} o no te pertenece."
        except Exception as e:
            return f"Error al eliminar el recordatorio: {e}"

    def mark_as_done(self, user_id: int, reminder_id_str: str) -> str:
        """Marca un recordatorio pendiente como completado."""
        if not reminder_id_str.isdigit():
            return "El ID del recordatorio debe ser numérico."
            
        reminder_id = int(reminder_id_str)
        try:
            success = self.repo.update_reminder_status(reminder_id, user_id, 'done')
            if success:
                return f"Recordatorio {reminder_id} marcado como completado."
            return f"No se encontró el recordatorio {reminder_id} o no te pertenece."
        except Exception as e:
            return f"Error al completar el recordatorio: {e}"
