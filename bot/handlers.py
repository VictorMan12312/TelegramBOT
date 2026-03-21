import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.reminder_service import ReminderService
from utils.formatter import format_reminders_list

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Enviar un mensaje cuando se emite el comando /start."""
    user = update.effective_user
    welcome_text = (
        f"¡Hola {user.first_name}!\n\n"
        "Soy tu bot de recordatorios. Aquí tienes los comandos disponibles:\n"
        "/add <texto> - Crea un nuevo recordatorio\n"
        "/list - Muestra tus recordatorios\n"
        "/update <id> <nuevo texto> - Actualiza un recordatorio especifico\n"
        "/done <id> - Marca un recordatorio como completado\n"
        "/delete <id> - Elimina un recordatorio"
    )
    await update.message.reply_text(welcome_text)

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = " ".join(context.args)
    
    if not text:
        await update.message.reply_text("Uso correcto: /add <texto de tu recordatorio>")
        return
        
    response = ReminderService.add_reminder(user_id, text)
    await update.message.reply_text(response)

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    success, result = ReminderService.get_user_reminders(user_id)
    
    if success:
        response = format_reminders_list(result)
        await update.message.reply_markdown(response)
    else:
        await update.message.reply_text(result)

async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    
    if len(args) < 2:
        await update.message.reply_text("Uso correcto: /update <id> <nuevo texto>")
        return
        
    reminder_id = args[0]
    new_text = " ".join(args[1:])
    
    response = ReminderService.update_reminder(user_id, reminder_id, new_text)
    await update.message.reply_text(response)

async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("Uso correcto: /done <id>")
        return
        
    reminder_id = args[0]
    response = ReminderService.mark_as_done(user_id, reminder_id)
    await update.message.reply_text(response)

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    
    if not args:
        await update.message.reply_text("Uso correcto: /delete <id>")
        return
        
    reminder_id = args[0]
    response = ReminderService.delete_reminder(user_id, reminder_id)
    await update.message.reply_text(response)
