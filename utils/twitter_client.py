# utils/twitter_client.py
import os
import tweepy
import requests
import logging
from datetime import datetime
from utils.tweet_generator import generate_natural_post

# ログ用ディレクトリを作成
os.makedirs("logs", exist_ok=True)
log_dir = "logs"
log_file = f"{log_dir}/bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def post_to_account(account):
    account_index = account.get('id', 'Unknown ID')

    # Tweepy v2 (テキスト投稿用)
    client = tweepy.Client(
        consumer_key=account["API_KEY"],
        consumer_secret=account["API_SECRET"],
        access_token=account["ACCESS_TOKEN"],
        access_token_secret=account["ACCESS_TOKEN_SECRET"],
    )
    logging.info(f"Account {account_index}: Posting to {account.get('screen_name', 'Unknown Screen Name')}")
    
    # Tweepy v1.1 (画像アップロード用)
    auth = tweepy.OAuth1UserHandler(
        account["API_KEY"], account["API_SECRET"],
        account["ACCESS_TOKEN"], account["ACCESS_TOKEN_SECRET"]
    )
    api_v1 = tweepy.API(auth)

    # ツイート本文と画像URLを生成
    tweet, picture_url = generate_natural_post(account, account_index)

    try:
        if debug_mode := os.getenv("DEBUG_MODE", "false").lower() == "true":
            logging.info(f"[DEBUG] Account {account_index}: {tweet}, Picture={picture_url}")
            return

        # 画像を必ず取得
        if not picture_url:
            logging.error(f"Account {account_index}: No picture URL received, aborting post.")
            return

        logging.info(f"Account {account_index}: Downloading image {picture_url}")
        response = requests.get(picture_url, stream=True)
        if response.status_code != 200:
            logging.error(f"Account {account_index}: Failed to download image")
            return

        # 一時ファイルに保存
        temp_filename = "temp_image.jpg"
        with open(temp_filename, "wb") as f:
            f.write(response.content)

        # 画像をアップロード
        media = api_v1.media_upload(temp_filename)
        media_ids = [media.media_id]

        # 一時ファイル削除
        os.remove(temp_filename)

        # ツイート投稿（必ず画像付き）
        response = client.create_tweet(text=tweet, media_ids=media_ids)
        logging.info(f"Account {account_index}: Posted with image: {tweet}")

    except Exception as e:
        logging.error(f"Account {account_index}: Error posting - {e}")
