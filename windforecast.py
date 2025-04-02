import requests
import time
from datetime import datetime, timedelta
from bot_module.bot_manager import *


# Configuración
API_KEY = weather_api_key  # Reemplaza con tu clave de OpenWeatherMap
LAT = -34.6  # Buenos Aires
LON = -58.4
CHECK_INTERVAL = 86400  # 24 horas en segundos
MAX_LIMIT = 50
MIN_LIMIT = 13

# Función para obtener el pronóstico
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&units=metric&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al obtener datos de OpenWeatherMap")
        return None

# Función para enviar mensaje por Telegram

# Función principal
def check_wind_conditions():
    data = get_weather()
    if not data:
        return
    
    message = "🌊 Pronóstico de viento para las próximas 72 horas:\n"
    now = datetime.utcnow()
    end_time = now + timedelta(hours=72)
    
    for forecast in data["list"]:
        timestamp = forecast["dt"]
        wind_speed = forecast["wind"]["speed"] * 1.94384  # Convertir m/s a nudos
        date = datetime.utcfromtimestamp(timestamp)
        
        if now <= date <= end_time and MIN_LIMIT <= wind_speed <= MAX_LIMIT:
            message += f"\n📅 {date.strftime('%Y-%m-%d %H:%M')} - {wind_speed:.2f} nudos"
    
    if "📅" in message:
        print(message)
        send_tm(message)
    else:
        send_tm("No hay condiciones favorables en las próximas 72 horas.")

while True:
    # Ejecutar periódicamente
    print(datetime.now())
    check_wind_conditions()
    print(f'sleeping {CHECK_INTERVAL/3600} hours...' )
    time.sleep(CHECK_INTERVAL)

