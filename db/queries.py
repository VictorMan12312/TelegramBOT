from typing import List, Optional
from db.connection import get_db_connection
from models.reminder import Reminder

def init_db():
    """Inicializa la base de datos creando la tabla necesaria."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            title TEXT NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def create_reminder(reminder: Reminder) -> int:
    """Inserta un nuevo recordatorio en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO reminders (user_id, title, status, due_date)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (reminder.user_id, reminder.title, reminder.status, reminder.due_date))
    conn.commit()
    inserted_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return inserted_id

def get_reminders_by_user(user_id: int) -> List[Reminder]:
    """Obtiene todos los recordatorios para un usuario específico."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM reminders WHERE user_id = %s ORDER BY created_at DESC"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [Reminder(**row) for row in rows]

def get_reminder_by_id_and_user(reminder_id: int, user_id: int) -> Optional[Reminder]:
    """Obtiene un recordatorio específico por ID y el ID del usuario."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM reminders WHERE id = %s AND user_id = %s"
    cursor.execute(query, (reminder_id, user_id))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if row:
        return Reminder(**row)
    return None

def update_reminder_title(reminder_id: int, user_id: int, new_title: str) -> bool:
    """Actualiza el título del recordatorio objetivo."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE reminders SET title = %s WHERE id = %s AND user_id = %s"
    cursor.execute(query, (new_title, reminder_id, user_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected > 0

def update_reminder_status(reminder_id: int, user_id: int, status: str) -> bool:
    """Actualiza el estado del recordatorio objetivo."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE reminders SET status = %s WHERE id = %s AND user_id = %s"
    cursor.execute(query, (status, reminder_id, user_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected > 0

def delete_reminder(reminder_id: int, user_id: int) -> bool:
    """Elimina el recordatorio dado."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "DELETE FROM reminders WHERE id = %s AND user_id = %s"
    cursor.execute(query, (reminder_id, user_id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    return affected > 0
