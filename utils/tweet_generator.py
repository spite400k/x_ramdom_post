# utils/tweet_generator.py
import logging
import openai
import os
import random
from datetime import datetime
from utils.weather import get_weather_context
from utils.time_context import get_time_context
from config.personality_profiles import PERSONALITY_PROFILES
from utils.trend_analyzer import get_google_trends

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

def generate_natural_post(account, account_index: int = 0) -> str:
    profile = PERSONALITY_PROFILES.get(account_index, {
        "name": f"Account{account_index + 1}",
        "tone": "自然で親しみやすい口調",
        "theme": "日常の出来事を話す"
    })

    # コンテキスト情報（天気・時間・トレンド）
    include_time = random.random() < 0.1
    include_weather = random.random() < 0.1
    include_trend = random.random() < 0.1

    time_ctx = get_time_context() if include_time else None
    weather_ctx = get_weather_context() if include_weather else None
    trend_ctx = get_google_trends(profile['theme'], account) if include_trend else None

    # 過去投稿の使用（10%）
    past_posts = load_previous_posts(account_index)
    use_past = past_posts and random.random() < 0.1
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
    好きなものは「{profile['theme']}」です。
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

    # #入力情報例
    # {profile['input'] if 'input' in profile else ''}

    # #出力例
    # {profile['output'] if 'output' in profile else ''}

    
    logging.info(f"[DEBUG] Prompt: {prompt.strip()}")
    try:
        response = openai.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI Error] {e}")
        return "今日も一日おつかれさまでした。"
