from abc import ABC, abstractmethod
from typing import List, Optional
from models.reminder import Reminder
import db.queries as queries

class ReminderRepository(ABC):
    """Interfaz abstracta para el repositorio de recordatorios."""
    
    @abstractmethod
    def create_reminder(self, reminder: Reminder) -> int:
        """Agrega un nuevo recordatorio al repositorio."""
        pass

    @abstractmethod
    def get_reminders_by_user(self, user_id: int) -> List[Reminder]:
        """Obtiene la lista de recordatorios de un usuario."""
        pass

    @abstractmethod
    def get_reminder_by_id_and_user(self, reminder_id: int, user_id: int) -> Optional[Reminder]:
        """Busca un recordatorio en específico por ID y usuario."""
        pass

    @abstractmethod
    def update_reminder_title(self, position: int, user_id: int, new_title: str) -> bool:
        """Modifica el texto principal de un recordatorio."""
        pass

    @abstractmethod
    def update_reminder_status(self, position: int, user_id: int, status: str) -> bool:
        """Modifica el estado (como 'done') de un recordatorio."""
        pass

    @abstractmethod
    def delete_reminder(self, position: int, user_id: int) -> bool:
        """Remueve un recordatorio del repositorio."""
        pass


class MySQLReminderRepository(ReminderRepository):
    """Implementación de ReminderRepository que utiliza base de datos MySQL."""

    def create_reminder(self, reminder: Reminder) -> int:
        return queries.create_reminder(reminder)

    def get_reminders_by_user(self, user_id: int) -> List[Reminder]:
        return queries.get_reminders_by_user(user_id)

    def get_reminder_by_id_and_user(self, reminder_id: int, user_id: int) -> Optional[Reminder]:
        return queries.get_reminder_by_id_and_user(reminder_id, user_id)

    def update_reminder_title(self, position: int, user_id: int, new_title: str) -> bool:
        return queries.update_reminder_title(position, user_id, new_title)

    def update_reminder_status(self, position: int, user_id: int, status: str) -> bool:
        return queries.update_reminder_status(position, user_id, status)

    def delete_reminder(self, position: int, user_id: int) -> bool:
        return queries.delete_reminder(position, user_id)
