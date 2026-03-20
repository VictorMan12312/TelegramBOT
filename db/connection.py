import os
import mysql.connector
from mysql.connector.connection import MySQLConnection

def get_db_connection() -> MySQLConnection:
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    La configuración se carga desde las variables de entorno.
    """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "reminder_db"),
        port=os.getenv("DB_PORT", "3306")
    )
    return connection
