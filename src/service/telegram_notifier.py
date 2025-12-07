import requests
from prefect import task
from src.config import TELEGRAM

@task
def notify(daily_stats: list):

    msg = "Прогноз погоды\n\n"

    for s in daily_stats:
        msg += (
            f"{s['city']}\n\n"
            f"Средняя температура: {s['avg_temp']:.1f}\n"
            f"Осадки: {s['total_precip']:.1f} мм\n"
            f"Ветер: до {s['max_wind']:.1f} км/ч\n\n"
        )

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM['token']}/sendMessage",
        json={"chat_id": TELEGRAM["chat_id"], "text": msg, "parse_mode": "Markdown"},
    )
