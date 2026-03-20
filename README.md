# Telegram Reminder Bot

Un bot de Telegram completo y profesional para la gestión de recordatorios. Desarrollado en Python, utiliza una arquitectura limpia, separando las responsabilidades por capas.

## Características
- Arquitectura Modular y Limpia.
- Base de datos MySQL.
- Funciones CRUD completas: Agregar, listar, actualizar, eliminar y marcar como completado.
- Manejo asíncrono con `python-telegram-bot`.
- Preparado para agregar tareas programadas a futuro (incluye campo `due_date`).

## Requisitos Previos
- Python 3.11+
- Servidor MySQL.
- Un bot creado en Telegram a través de BotFather (para obtener el Token).

## Instalación

1. Clona el repositorio o extrae los archivos del proyecto.
2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate
   venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Copia el archivo de ejemplo de variables de entorno y configúralo:
   ```bash
   cp .env.example .env
   ```
   Edita `.env` y agrega tu token de Telegram y credenciales de la base de datos MySQL (Asegúrate de haber creado la base de datos `reminder_db` o el nombre que configures).

## Base de datos
El bot crea automáticamente la tabla `reminders` en la base de datos la primera vez que se ejecuta, siempre que la cuenta de MySQL tenga los permisos adecuados y la base de datos especificada en `.env` ya exista.

## Uso y Comandos del Bot
Inicia el bot ejecutando el módulo principal (desde la raíz del proyecto):
```bash
python -m bot.main
```

- `/start` - Muestra el mensaje de bienvenida y comandos disponibles.
- `/add <texto>` - Crea un nuevo recordatorio.
- `/list` - Lista todos tus recordatorios activos y completados.
- `/update <id> <nuevo texto>` - Cambia el texto de un recordatorio específico.
- `/done <id>` - Marca un recordatorio como completado.
- `/delete <id>` - Elimina un recordatorio.
