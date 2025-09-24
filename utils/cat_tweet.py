import random

import requests
from config.search_word import SEARCH_WORDS
import os
import logging
from datetime import datetime

# ログ設定
# ログ用ディレクトリを作成（存在しなければ）
log_dir = "logs"
log_file = f"{log_dir}/bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# ---------------------
# Unsplash APIキー
# ---------------------
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


# ---------------------
# Unsplashから猫画像を取得
# ---------------------
def get_random_cat_image(query="cat"):

    url = "https://api.unsplash.com/photos/random"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {"query": query, "orientation": "landscape"}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return data["urls"]["regular"], data["user"]["name"], data["links"]["html"]
    except Exception as e:
        logging.error(f"[Unsplash Error] {e}")
        return None, None, None
    
# ---------------------
# 猫画像付きツイート生成
# ---------------------
def generate_cat_tweet(account_index: int):
    word = SEARCH_WORDS.get(account_index)
    img_url, photographer, photo_link = get_random_cat_image(word['picture'] if word else "cat")

    hashtags = word['hashtags'] if word else []
    if img_url:
        # tweet_text_with_hashtags = random.sample(hashtags, random.randint(2, 3))

        selected = random.sample(hashtags, min(2, len(hashtags)))
        tweet_text_with_hashtags = " ".join(selected)

        return tweet_text_with_hashtags, img_url
    else:
        return None, None