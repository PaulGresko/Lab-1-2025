import requests
from prefect import task
from src.utils import tomorrow_str

@task(retries=3)
def fetch_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,wind_speed_10m,wind_direction_10m",
        "start_date": tomorrow_str(),
        "end_date": tomorrow_str(),
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
