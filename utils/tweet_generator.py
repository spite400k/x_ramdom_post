# utils/tweet_generator.py
import openai
import os
import random
from datetime import datetime
from utils.weather import get_weather_context
from utils.time_context import get_time_context
from config.personality_profiles import PERSONALITY_PROFILES

openai.api_key = os.getenv("OPENAI_API_KEY")

def load_previous_posts(account_index: int) -> str:
    path = f"data/account{account_index + 1}_posts.txt"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        return ""
    samples = random.sample(lines, min(3, len(lines)))
    return "".join(samples)

def generate_natural_post(account_index: int) -> str:
    time_ctx = get_time_context()
    past_posts = load_previous_posts(account_index)

    profile = PERSONALITY_PROFILES.get(account_index, {
        "tone": "自然で親しみやすい口調",
        "theme": "日常の出来事を話す"
    })

    # 天気情報を含める確率10%
    include_weather = random.random() < 0.1
    weather_ctx = get_weather_context() if include_weather else None

    prompt = (
        f"{profile['name']}というキャラクターとして投稿を作成してください。\n"
        f"投稿は{profile['theme']}が中心で、口調は{profile['tone']}です。\n"
        f"今の時刻は{time_ctx}です。" +
        (f" 天気は{weather_ctx}です。" if include_weather and weather_ctx else "") +
        "\n\n"
        f"以下の過去投稿のスタイルを参考にしてください。\n"
        f"【過去投稿例】\n{past_posts}\n\n"
        f"【新しい投稿】：140文字以内で自然なX投稿を1つ生成してください。"
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI Error] {e}")
        return "今日も一日おつかれさまでした。"
