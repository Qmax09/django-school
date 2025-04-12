
import requests

TELEGRAM_TOKEN = "7728998314:AAFUH449r3zHRTE3B4Vi7fNvaqNAxHNprQY"

# Список получателей
CHAT_IDS = [
    "1025070656",  # Adil
    "1121477210",  # Dimash
    "1034373297",  # Мейрбек
]

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    success = True
    for chat_id in CHAT_IDS:
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        if response.status_code != 200:
            success = False
    return success

