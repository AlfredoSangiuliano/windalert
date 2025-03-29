import requests
from bot_module.secret_vault import *

def send_tm(message):
    chat_id
    bot_token
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    return response.json()
