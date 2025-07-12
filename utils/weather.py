# utils/time_context.py
from datetime import datetime

def get_time_context() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 10:
        return "朝"
    elif 10 <= hour < 16:
        return "昼"
    elif 16 <= hour < 19:
        return "夕方"
    elif 19 <= hour < 23:
        return "夜"
    else:
        return "深夜"


# utils/weather.py
import os
import requests

def get_weather_context(city="Tokyo") -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "天気情報は不明"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ja&units=metric"
        res = requests.get(url).json()
        description = res["weather"][0]["description"]
        temp = res["main"]["temp"]
        return f"{description}で気温は{int(temp)}度"
    except Exception as e:
        print(f"[Weather Error] {e}")
        return "天気情報の取得に失敗"
