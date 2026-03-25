import re
from datetime import datetime, timedelta

def parse_natural_language(text):
    """
    Procesa un texto en lenguaje natural para extraer marcas temporales como 
    'mañana', 'en X horas' o 'HH:MM'. Retorna el texto limpio y el objeto datetime.
    """
    text = text.lower()
    now = datetime.now()

    if "mañana" in text:
        date = now + timedelta(days=1)
    else:
        date = now

    match_hours = re.search(r'en (\d+) horas?', text)
    if match_hours:
        hours = int(match_hours.group(1))
        return {
            "title": text,
            "datetime": now + timedelta(hours=hours)
        }

    match_time = re.search(r'(\d{1,2})(:\d{2})?', text)
    if match_time:
        hour = int(match_time.group(1))
        minute = 0

        if match_time.group(2):
            minute = int(match_time.group(2)[1:])

        date = date.replace(hour=hour, minute=minute, second=0)

    clean_text = re.sub(r'(mañana|en \d+ horas?)', '', text)

    return {
        "title": clean_text.strip(),
        "datetime": date
    }