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
        send_tm(f"Error al obtener datos de OpenWeatherMap. Error:{response.status_code} {response.json()['message']}")
        return None

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
        wind_deg = forecast["wind"]["deg"]  # Dirección del viento en grados
        date = datetime.utcfromtimestamp(timestamp)
        
        if now <= date <= end_time and MIN_LIMIT <= wind_speed <= MAX_LIMIT:
            direction = get_wind_direction(wind_deg)
            message += f"\n📅 {date.strftime('%Y-%m-%d %H:%M')} - {wind_speed:.2f} nudos - Dirección: {direction}"
    
    if "📅" in message:
        send_tm(message)
    else:
        send_tm("No hay condiciones favorables en las próximas 72 horas.")


def get_wind_direction(deg):
    if 0 <= deg < 45 or 315 <= deg < 360:
        return "Norte"
    elif 45 <= deg < 90:
        return "Noreste"
    elif 90 <= deg < 135:
        return "Este"
    elif 135 <= deg < 180:
        return "Sureste"
    elif 180 <= deg < 225:
        return "Sur"
    elif 225 <= deg < 270:
        return "Suroeste"
    elif 270 <= deg < 315:
        return "Oeste"
    else:
        return "Noroeste"

while True:
    # Ejecutar periódicamente
    print(datetime.now())
    check_wind_conditions()
    send_tm(f'sleeping {CHECK_INTERVAL/3600} hours...' )
    time.sleep(CHECK_INTERVAL)

