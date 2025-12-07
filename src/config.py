import os
from dotenv import load_dotenv

load_dotenv()

MINIO_BUCKET = "weather-data"

CLICKHOUSE = {
    "host": "localhost",
    "port": 8123,
    "user": "default",
    "password": "",
    "db": "weather_db",
}

TELEGRAM = {
    "token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
}

CITIES = {
    "Moscow": {"lat": 55.7558, "lon": 37.6173, "ru_name": "Москва"},
    "Samara": {"lat": 53.1959, "lon": 50.1002, "ru_name": "Самара"},
}
