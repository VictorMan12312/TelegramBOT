import os
import logging
import sys

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Importaciones de la aplicación dependientes de entorno
from telegram.ext import Application, CommandHandler
from db.queries import init_db
from bot.handlers import (
    start_command,
    add_command,
    list_command,
    update_command,
    done_command,
    delete_command
)

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Nivel de registro HTTPx ajustado para reducir el ruido
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def main() -> None:
    """Iniciar el bot."""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token or token == "tu_token_aqui":
        logger.error("No se proporcionó TELEGRAM_TOKEN en el archivo .env.")
        sys.exit(1)

    # Inicializar la base de datos
    logger.info("Inicializando la base de datos...")
    try:
        init_db()
        logger.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        # Detener ejecución si falla la inicialización de la base de datos
        sys.exit(1)

    # Crear la aplicación y pasarle el token
    application = Application.builder().token(token).build()

    # Configuración de manejadores de comandos
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("update", update_command))
    application.add_handler(CommandHandler("done", done_command))
    application.add_handler(CommandHandler("delete", delete_command))

    # Iniciar el polling del bot
    logger.info("Iniciando el bot en modo polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
