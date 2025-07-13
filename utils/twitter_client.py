# utils/twitter_client.py
import tweepy
from utils.tweet_generator import generate_natural_post
from datetime import datetime
import logging

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

def post_to_account(account, account_index):
    client = tweepy.Client(
        consumer_key=account["API_KEY"],
        consumer_secret=account["API_SECRET"],
        access_token=account["ACCESS_TOKEN"],
        access_token_secret=account["ACCESS_TOKEN_SECRET"],
    )

    tweet = generate_natural_post(account_index)
    try:
        response = client.create_tweet(text=tweet)
        logging.info(f"Account {account_index + 1}: Posted: {tweet}")
    except Exception as e:
        logging.error(f"Account {account_index + 1}: Error posting - {e}")
