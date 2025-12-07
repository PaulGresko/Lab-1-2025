import pandas as pd
from prefect import flow
from config import CITIES
from src.service.weather_api import fetch_weather
from src.service.minio_writer import save_raw_to_minio
from src.service.clickhouse_loader import load_hourly, load_daily
from src.service.telegram_notifier import notify


def process_hourly(city: str, raw: dict) -> pd.DataFrame:
    h = raw["hourly"]
    return pd.DataFrame({
        "city": city,
        "forecast_time": pd.to_datetime(h["time"]),
        "temperature": h["temperature_2m"],
        "precipitation": h["precipitation"],
        "wind_speed": h["wind_speed_10m"],
        "wind_direction": h["wind_direction_10m"],
    })


def calc_daily_stats(city_ru: str, df: pd.DataFrame) -> dict:
    return {
        "city": city_ru,
        "forecast_date": df["forecast_time"].dt.date.iloc[0],
        "min_temp": float(df["temperature"].min()),
        "max_temp": float(df["temperature"].max()),
        "avg_temp": float(df["temperature"].mean()),
        "total_precip": float(df["precipitation"].sum()),
        "max_wind": float(df["wind_speed"].max()),
    }


@flow(name="weather_etl")
def weather_flow():
    results = []

    for city, meta in CITIES.items():
        raw = fetch_weather(meta["lat"], meta["lon"])
        save_raw_to_minio(city, raw)

        df = process_hourly(city, raw)
        stats = calc_daily_stats(meta["ru_name"], df)

        load_hourly(df)
        load_daily(stats)

        results.append(stats)

    notify(results)


if __name__ == "__main__":
    weather_flow()
