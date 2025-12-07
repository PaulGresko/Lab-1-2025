import pandas as pd
import clickhouse_connect
from prefect import task
from src.config import CLICKHOUSE

def get_client():
    return clickhouse_connect.get_client(
        host=CLICKHOUSE["host"],
        port=CLICKHOUSE["port"],
        username=CLICKHOUSE["user"],
        password=CLICKHOUSE["password"],
    )

HOURLY_COLUMN_NAMES = [
            "city",
            "datetime",
            "temperature",
            "precipitation",
            "wind_speed",
            "wind_direction"
        ]

DAILY_COLUMN_NAMES =[
    "city",
    "date",
    "min_temp",
    "max_temp",
    "avg_temp",
    "precipitation_sum"
]

@task
def load_hourly(df: pd.DataFrame):
    client = get_client()
    table = f"{CLICKHOUSE['db']}.weather_hourly"

    client.insert(
        table,
        df[[
            "city",
            "datetime",
            "temperature",
            "precipitation",
            "wind_speed",
            "wind_direction"
        ]].values.tolist(),
        HOURLY_COLUMN_NAMES,
    )

@task
def load_daily(stats: dict):
    client = get_client()
    table = f"{CLICKHOUSE['db']}.weather_daily"

    client.insert(
        table,
        [[
            stats["city"],
            stats["date"],
            stats["min_temp"],
            stats["max_temp"],
            stats["avg_temp"],
            stats["precipitation_sum"],
        ]],
        DAILY_COLUMN_NAMES,
    )
