from requests_html import HTMLSession, HTML
import time
from pprint import pprint
from pathlib import Path
import pendulum
from nitter_scraper import get_tweets

root_dir = Path(__file__).parent
user_path = root_dir / "example.txt"

with open(user_path, mode="r") as f:
    users = f.read().strip().split("\n")

for user in users:
    for tweets in get_tweets(user, pages=25):
        for tweet in tweets:
            print(tweet)
            print(tweet.json())
