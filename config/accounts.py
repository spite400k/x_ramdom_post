import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNTS = [
    {
        "id": "1",
        "enabled": True,
        "screen_name": "yuki23675786",
        "API_KEY": os.getenv("API_KEY_1"),
        "API_SECRET": os.getenv("API_SECRET_KEY_1"),
        "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN_1"),
        "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET_1"),
    },
    {
        "id": "2",
        "enabled": True,
        "screen_name": "Ren47291",
        "API_KEY": os.getenv("API_KEY_2"),
        "API_SECRET": os.getenv("API_SECRET_KEY_2"),
        "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN_2"),
        "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET_2"),
    },
    {
        "id": "3",
        "enabled": True,
        "screen_name": "Sora36100",
        "API_KEY": os.getenv("API_KEY_3"),
        "API_SECRET": os.getenv("API_SECRET_KEY_3"),
        "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN_3"),
        "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET_3"),
    },
    {
        "id": "4",
        "enabled": True,
        "screen_name": "AdultSelectLab",
        "API_KEY": os.getenv("API_KEY_4"),
        "API_SECRET": os.getenv("API_SECRET_KEY_4"),
        "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN_4"),
        "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET_4"),
    },
]
