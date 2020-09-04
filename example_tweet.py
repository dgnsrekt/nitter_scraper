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
    for idx, tweet in enumerate(get_tweets(user, pages=100)):
        print()
        pprint(tweet.to_dict())
        print(tweet.to_json())
        pprint(tweet.to_tuple())
