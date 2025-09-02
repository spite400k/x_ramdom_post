# utils/twitter_client.py
import os
import tweepy
from utils.tweet_generator import generate_natural_post
from datetime import datetime
import logging

# ログ用ディレクトリを作成（存在しなければ）
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
    client = tweepy.Client(
        consumer_key=account["API_KEY"],
        consumer_secret=account["API_SECRET"],
        access_token=account["ACCESS_TOKEN"],
        access_token_secret=account["ACCESS_TOKEN_SECRET"],
    )
    logging.info(f"Account {account_index}: Posting to {account.get('screen_name', 'Unknown Screen Name')}")
    tweet = generate_natural_post(account, account_index)
    try:
        if debug_mode := os.getenv("DEBUG_MODE", "false").lower() == "true":
            logging.info(f"[DEBUG] Account {account_index}: {tweet}")
            return
        response = client.create_tweet(text=tweet)
        logging.info(f"Account {account_index}: Posted: {tweet}")
    except Exception as e:
        logging.error(f"Account {account_index}: Error posting - {e}")
