import os
import logging
import sys
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv
from telegram.ext import MessageHandler, filters

load_dotenv()

from db.queries import init_db
from db.repository import MySQLReminderRepository
from services.reminder_service import ReminderService
from bot.handlers import BotHandlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def main() -> None:
    """Inicia el bot, configura la base de datos e inyecta las dependencias necesarias."""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token or token == "tu_token_aqui":
        logger.error("No se proporcionó TELEGRAM_TOKEN en el archivo .env.")
        sys.exit(1)

    logger.info("Inicializando la base de datos...")
    try:
        init_db()
        logger.info("Base de datos inicializada correctamente.")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        sys.exit(1)

    application = ApplicationBuilder().token(token).build()
    
    job_queue = application.job_queue
    repo = MySQLReminderRepository()
    service = ReminderService(job_queue, repo)
    handlers = BotHandlers(service)

    application.add_handler(CommandHandler("start", handlers.start_command))
    application.add_handler(CommandHandler("add", handlers.add_command))
    application.add_handler(CommandHandler("list", handlers.list_command))
    application.add_handler(CommandHandler("update", handlers.update_command))
    application.add_handler(CommandHandler("done", handlers.done_command))
    application.add_handler(CommandHandler("delete", handlers.delete_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.message_handler))

    logger.info("Iniciando el bot en modo polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
