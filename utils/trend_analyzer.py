# utils/trend_analyzer.py

import logging
import os
import random
import tweepy
import feedparser
from dotenv import load_dotenv

load_dotenv()

# WOEID（日本 = 23424856）
JAPAN_WOEID = 23424856

def get_trending_topics(theme=None, account=None, woeid=JAPAN_WOEID, top_n=10) -> list[str]:
    if not account:
        logging.warning("Twitter API認証情報が不足しています。")
        return []

    try:
        auth = tweepy.OAuth1UserHandler(
            consumer_key=account["API_KEY"],
            consumer_secret=account["API_SECRET"],
            access_token=account["ACCESS_TOKEN"],
            access_token_secret=account["ACCESS_TOKEN_SECRET"]
        )
        api = tweepy.API(auth)
        trends = api.get_place_trends(woeid)
        trend_list = trends[0]['trends']
        sorted_trends = sorted(trend_list, key=lambda t: t.get("tweet_volume") or 0, reverse=True)
        return [t['name'] for t in sorted_trends[:top_n]]
    except Exception as e:
        logging.error(f"[TwitterTrend Error] {e}")
        return []

def get_google_trends_fallback() -> str:
    try:
        url = 'https://trends.google.com/trendingsearches/daily/rss?geo=JP'
        feed = feedparser.parse(url)
        if not feed.entries:
            logging.warning("[GoogleTrends RSS] フィードが空です。")
            return ""
        selected = random.choice(feed.entries)
        return selected.title
    except Exception as e:
        logging.error(f"[GoogleTrends RSS Error] {e}")
        return ""

def get_google_trends(theme=None, account=None) -> str:
    """Twitter API → Google RSS fallbackの順でトレンド取得"""
    # twitter_trends = get_trending_topics(theme=theme, account=account)
    # if twitter_trends:
    #     return random.choice(twitter_trends)
    
    # Fallback to Google Trends RSS
    return get_google_trends_fallback()
