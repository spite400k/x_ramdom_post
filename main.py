# main.py
import os
import logging
import time
from datetime import datetime
from zoneinfo import ZoneInfo 
import random
from utils.twitter_client import post_to_account
from config.accounts import ACCOUNTS

# ログ設定
# ログ用ディレクトリを作成（存在しなければ）
os.makedirs("logs", exist_ok=True)  
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

# 投稿許可時間帯かどうか（7:00〜21:59 JST）
def is_within_posting_hours():
    jst_now = datetime.now(ZoneInfo("Asia/Tokyo"))
    return 7 <= jst_now.hour < 22

def main():
    if not is_within_posting_hours():
        logging.info("現在は投稿許可時間外（7:00〜21:59）です。スキップします。")
        return

    for account in ACCOUNTS:

        if not account["enabled"]:
            logging.warning(f"⚠️ {account['screen_name']} は実施フラグOFFのためスキップします")
            continue
            

        logging.info(f"\n--- Posting for Account {account['id']} - {account['screen_name']} ---")
        wait_minutes = random.randint(1, 10)  # 1分〜10分のランダム
        # wait_minutes=1
        logging.info(f"Account {account['id']} - {account['screen_name']}: {wait_minutes}分待機してから投稿します")
        time.sleep(wait_minutes * 60)
        try:
            # post_to_account(account)
            logging.info(f"Account {account['id']} - {account['screen_name']}: 投稿成功")
        except Exception as e:
            logging.error(f"Account {account['id']} - {account['screen_name']}: 投稿失敗 - {e}")

if __name__ == "__main__":
    main()
