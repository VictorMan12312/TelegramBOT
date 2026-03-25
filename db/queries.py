from typing import List, Optional
from db.connection import get_db_connection
from models.reminder import Reminder
import logging

logger = logging.getLogger(__name__)

def init_db():
    """Inicializa la base de datos creando la tabla de recordatorios si no existe."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            position INT NOT NULL,
            title TEXT NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date DATETIME NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def create_reminder(reminder: Reminder) -> int:
    """
    Inserta un nuevo recordatorio en la base de datos incrementando la posición.
    Retorna la posición generada, la cual actúa como ID relativo para el usuario.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COALESCE(MAX(position), 0) FROM reminders WHERE user_id = %s", (reminder.user_id,))
    last_position = cursor.fetchone()[0]
    new_position = last_position + 1
    
    query = """
        INSERT INTO reminders (user_id, position, title, status, due_date)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (reminder.user_id, new_position, reminder.title, reminder.status, reminder.due_date))
    conn.commit()
    
    inserted_id = new_position 
    cursor.close()
    conn.close()
    return inserted_id

def get_reminders_by_user(user_id: int) -> List[Reminder]:
    """Obtiene todos los recordatorios para un usuario ordenados por posición."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM reminders WHERE user_id = %s ORDER BY position ASC, created_at DESC"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [Reminder(**row) for row in rows]

def get_reminder_by_id_and_user(reminder_id: int, user_id: int) -> Optional[Reminder]:
    """Obtiene un recordatorio específico utilizando su posición (ID) y el ID del usuario."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM reminders WHERE position = %s AND user_id = %s"
    cursor.execute(query, (reminder_id, user_id))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if row:
        return Reminder(**row)
    return None

def update_reminder_title(position: int, user_id: int, new_title: str) -> bool:
    """Actualiza solo el texto/título del recordatorio a partir de su posición."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE reminders SET title = %s WHERE position = %s AND user_id = %s"
    cursor.execute(query, (new_title, position, user_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected > 0

def update_reminder_status(position: int, user_id: int, status: str) -> bool:
    """
    Actualiza el estado de un recordatorio (ej. 'done').
    Si es completado, reasigna su posición a 0 y reindexa los posteriores.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE reminders SET status = %s WHERE position = %s AND user_id = %s"
    cursor.execute(query, (status, position, user_id))
    affected = cursor.rowcount
    
    if status == 'done' and affected > 0:
        query_zero = "UPDATE reminders SET position = 0 WHERE position = %s AND user_id = %s AND status = 'done'"
        cursor.execute(query_zero, (position, user_id))
        query_reindex = "UPDATE reminders SET position = position - 1 WHERE position > %s AND user_id = %s AND position > 0"
        cursor.execute(query_reindex, (position, user_id))

    conn.commit()
    cursor.close()
    conn.close()
    return affected > 0

def delete_reminder(position: int, user_id: int) -> bool:
    """Elimina permanentemente un recordatorio y reindexa la posición de los restantes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM reminders WHERE position = %s AND user_id = %s"
    cursor.execute(query, (position, user_id))
    affected = cursor.rowcount
    
    if affected > 0:
        query_reindex = "UPDATE reminders SET position = position - 1 WHERE position > %s AND user_id = %s AND position > 0"
        cursor.execute(query_reindex, (position, user_id))
        
    conn.commit()
    cursor.close()
    conn.close()
    return affected > 0
