from datetime import date, timedelta

def tomorrow_str() -> str:
    return (date.today() + timedelta(days=1)).isoformat()
