# utils/tweet_generator.py
import logging
import openai
import os
import random
import requests
from datetime import datetime
from utils.weather import get_weather_context
from utils.time_context import get_time_context
from config.personality_profiles import PERSONALITY_PROFILES
from utils.trend_analyzer import get_google_trends

openai.api_key = os.getenv("OPENAI_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

hashtags = [
    "#フォロバ",
    "#フォローした人全員フォロバする",
    "#相互フォロー",
    "#フォロバ100",
    "#フォロバ100％",
    "#フォロバ絶対",
    "#フォロバ支援",
    "#フォロバ率100",
    "#フォロー歓迎",
    "#相互希望",
    "#フォロバ希望",
    "#フォロバお願いします"
]

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
# 過去投稿読み込み
# ---------------------
def load_previous_posts(account_index: int) -> str:
    path = f"data/account{account_index}_posts.txt"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return ""
    samples = random.sample(lines, min(3, len(lines)))
    return "".join(samples)

# ---------------------
# 投稿生成
# ---------------------
def generate_natural_post(account, account_index: int = 0):
    profile = PERSONALITY_PROFILES.get(account_index)

    include_picture = random.random() < 0.5  # 50%で猫画像を付ける
    if include_picture:
        # 猫画像をUnsplashから取得
        img_url, photographer, photo_link = get_random_cat_image("cute cat")

        if img_url:
            tweet_text_with_hashtags = (
                f"今日のにゃんこ🐱 {profile['input'] if 'input' in profile else ''}\n\n"
                f"#猫好き #猫のいる生活\n"
                f"Photo by {photographer} on Unsplash: {photo_link}"
            )
            return tweet_text_with_hashtags, img_url
        else:
            # フォールバック（画像なし）
            include_picture = False

    if not include_picture:
        # コンテキスト情報（天気・時間・トレンド）
        include_time = random.random() < 0.1
        include_weather = random.random() < 0.1
        include_trend = random.random() < 0.1
        include_theme = random.random() < 0.1

        time_ctx = get_time_context() if include_time else None
        weather_ctx = get_weather_context() if include_weather else None
        trend_ctx = get_google_trends(profile['theme'], account) if include_trend else None

        # 過去投稿の使用（1%）
        past_posts = load_previous_posts(account_index)
        use_past = past_posts and random.random() < 0.01
        if use_past:
            past_posts = f"過去の投稿例:\n{past_posts}\n"
        else:
            past_posts = ""

        # 長さをランダム化（最大140文字）
        max_len = random.randint(10, 50)

        # プロンプト組み立て
        prompt = f"""
        #命令
        あなたは{profile['name']}というキャラクターです。
        口調は{profile['tone']}です。
        好きなものは「{profile['theme']  if include_theme else ''}」です。
        投稿内容は自然で親しみやすいものにしてください。
        
        #制約条件
        {profile['conditions'] if 'conditions' in profile else ''}
        Xに投稿する文章を{max_len}文字以内で1つ作成してください。
        「新しい投稿：」などの見出しは不要です。
        「」や""などの記号も不要です。

        #話題のヒント
        {f'今の時刻は{time_ctx}です。' if time_ctx else ''}
        {f'天気は{weather_ctx}です。' if weather_ctx else ''}
        {f'現在話題のトピック: {trend_ctx}' if trend_ctx else ''}
        {past_posts}
        """

        logging.info(f"[DEBUG] Prompt: {prompt.strip()}")
        try:
            response = openai.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )

            tweet_text = response.choices[0].message.content.strip()
            selected_hashtags = random.sample(hashtags, 2)
            tweet_text_with_hashtags = tweet_text + "\n\n" + " ".join(selected_hashtags)
            return tweet_text_with_hashtags, None

        except Exception as e:
            logging.error(f"[OpenAI Error] {e}")
            return "今日も一日おつかれさまでした。", None
