import os
import mysql.connector
from mysql.connector import pooling

_pool = None

def get_connection_pool():
    global _pool
    if _pool is None:
        _pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="reminder_pool",
            pool_size=5,
            pool_reset_session=True,
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "reminder_db"),
            port=int(os.getenv("DB_PORT", "3306"))
        )
    return _pool

def get_db_connection():
    """
    Obtiene una conexión a la base de datos desde el pool de conexiones.
    """
    connection_pool = get_connection_pool()
    return connection_pool.get_connection()