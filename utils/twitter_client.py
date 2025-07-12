# utils/twitter_client.py
import tweepy
from utils.tweet_generator import generate_natural_post
from datetime import datetime

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
        print(f"[{datetime.now()}] Account {account_index+1} Posted: {tweet}")
    except Exception as e:
        print(f"[{datetime.now()}] Error posting for Account {account_index+1}: {e}")
