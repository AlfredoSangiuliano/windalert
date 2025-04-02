import requests
import os

chat_id = os.getenv("CHAT_ID")
bot_token = os.getenv("BOT_TOKEN")
weather_api_key = os.getenv("API_KEY")

def send_tm(message):
    print(message)
    chat_id
    bot_token
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    return response.json()
