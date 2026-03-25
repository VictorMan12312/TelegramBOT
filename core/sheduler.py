def schedule_reminder(job_queue, user_id, chat_id, text, due_date):
    """Programa la ejecución de un recordatorio en la cola de trabajos (job_queue)."""
    job_queue.run_once(
        callback=send_reminder,
        when=due_date,
        data={
            "chat_id": chat_id,
            "text": text
        }
    )

async def send_reminder(context):
    """Callback que envía el mensaje del recordatorio al usuario cuando llega la fecha."""
    job_data = context.job.data

    await context.bot.send_message(
        chat_id=job_data["chat_id"],
        text=f"Recordatorio:\n{job_data['text']}"
    )