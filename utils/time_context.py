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
