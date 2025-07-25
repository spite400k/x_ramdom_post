from datetime import datetime
from zoneinfo import ZoneInfo 

def get_time_context() -> str:
    jst_now = datetime.now(ZoneInfo("Asia/Tokyo"))
    hour = jst_now.hour
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
