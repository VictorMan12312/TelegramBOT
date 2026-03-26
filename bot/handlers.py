import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.reminder_service import ReminderService
from utils.formatter import format_reminders_list
from ML.intent_model import predict_intent


logger = logging.getLogger(__name__)

class BotHandlers:
    """Clase para manejar los comandos de Telegram y delegar la lógica al servicio."""
    def __init__(self, service: ReminderService):
        self.service = service

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Envía un mensaje de bienvenida con los comandos disponibles al usar /start."""
        user = update.effective_user
        welcome_text = (
            f"Hola {user.first_name}!\n\n"
            "Soy tu bot de recordatorios. Aquí tienes los comandos disponibles:\n"
            "/add <texto> - Crea un nuevo recordatorio\n"
            "/list - Muestra tus recordatorios\n"
            "/update <id> <nuevo texto> - Actualiza un recordatorio especifico\n"
            "/done <id> - Marca un recordatorio como completado\n"
            "/delete <id> - Elimina un recordatorio"
        )
        await update.message.reply_text(welcome_text)

    async def add_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Crea un nuevo recordatorio con el texto proporcionado."""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        text = " ".join(context.args)
        
        if not text:
            await update.message.reply_text("Uso correcto: /add <texto de tu recordatorio>")
            return
            
        result = self.service.add_reminder(user_id, chat_id, text)
        if result["success"]:
            await update.message.reply_text("Recordatorio programado")
        else:
            await update.message.reply_text(result["error"])

    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muestra la lista de recordatorios pendientes y completados del usuario."""
        user_id = update.effective_user.id
        success, result = self.service.get_user_reminders(user_id)
        
        if success:
            response = format_reminders_list(result)
            await update.message.reply_markdown(response)
        else:
            await update.message.reply_text(result)

    async def update_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Actualiza el texto de un recordatorio existente."""
        user_id = update.effective_user.id
        args = context.args
        
        if len(args) < 2:
            await update.message.reply_text("Uso correcto: /update <id> <nuevo texto>")
            return
            
        reminder_id = args[0]
        new_text = " ".join(args[1:])
        
        response = self.service.update_reminder(user_id, reminder_id, new_text)
        await update.message.reply_text(response)

    async def done_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Marca un recordatorio específico como completado."""
        user_id = update.effective_user.id
        args = context.args
        
        if not args:
            await update.message.reply_text("Uso correcto: /done <id>")
            return
            
        reminder_id = args[0]
        response = self.service.mark_as_done(user_id, reminder_id)
        await update.message.reply_text(response)

    async def delete_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Elimina un recordatorio específico."""
        user_id = update.effective_user.id
        args = context.args
        
        if not args:
            await update.message.reply_text("Uso correcto: /delete <id>")
            return
            
        reminder_id = args[0]
        response = self.service.delete_reminder(user_id, reminder_id)
        await update.message.reply_text(response)

    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if not text:
            return
            
        intent = predict_intent(text)
        if intent == "add":
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id
            result = self.service.add_reminder(user_id, chat_id, text)
            if result["success"]:
                await update.message.reply_text("Recordatorio programado")
            else:
                await update.message.reply_text(result["error"])
        elif intent == "list":
            await self.list_command(update, context)
        elif intent == "delete":
            await update.message.reply_text("Para eliminar usa el comando: /delete <id>")
        elif intent == "done":
            await update.message.reply_text("Para completar usa el comando: /done <id>")
        elif intent == "update":
            await update.message.reply_text("Para actualizar usa el comando: /update <id> <nuevo texto>")
        else:
            await update.message.reply_text("No entendí tu mensaje, intenta de nuevo")
    