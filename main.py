# main.py
import logging
import time
from datetime import datetime
import random
from utils.twitter_client import post_to_account
from config.accounts import ACCOUNTS

# ログ設定
log_dir = "logs"
log_file = f"{log_dir}/bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

import os
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 投稿許可時間帯かどうか（7:00〜21:59）
def is_within_posting_hours():
    now_hour = datetime.now().hour
    return 7 <= now_hour < 22

def main():
    if not is_within_posting_hours():
        logging.info("現在は投稿許可時間外（7:00〜21:59）です。スキップします。")
        return

    for idx, account in enumerate(ACCOUNTS):
        logging.info(f"\n--- Posting for Account {idx + 1} ---")
        wait = random.randint(60, 60 * 60)  # 1分〜60分のランダム
        logging.info(f"Account {idx + 1}: {wait // 60}分待機してから投稿します")
        time.sleep(wait)
        try:
            post_to_account(account, idx)
            logging.info(f"Account {idx + 1}: 投稿成功")
        except Exception as e:
            logging.error(f"Account {idx + 1}: 投稿失敗 - {e}")

if __name__ == "__main__":
    main()
