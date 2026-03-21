from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Reminder:
    """
    Modelo que representa una entidad Recordatorio en el sistema.
    """
    id: Optional[int]
    user_id: int
    title: str
    status: str
    position: Optional[int] = None
    created_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
