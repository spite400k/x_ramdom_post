# main.py
from utils.twitter_client import post_to_account
from config.accounts import ACCOUNTS
import time, random


def main():
    for idx, account in enumerate(ACCOUNTS):
        print(f"\n--- Posting for Account {idx + 1} ---")
        # post_count = random.randint(1, 2)
        post_count=1
        for i in range(post_count):
            wait = random.randint(60, 60 * 60 * 3)
            # wait=1
            print(f"Account {idx+1}: Waiting {wait//60} min before post {i+1}")
            time.sleep(wait)
            post_to_account(account, idx)


if __name__ == "__main__":
    main()
