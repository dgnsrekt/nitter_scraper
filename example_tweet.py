from requests_html import HTMLSession, HTML

import time
from pprint import pprint
from pathlib import Path
import pendulum
from nitter_scraper import get_tweets
from nitter_scraper import NitterDockerContainer

root_dir = Path(__file__).parent
user_path = root_dir / "example_users.txt"

with open(user_path, mode="r") as f:
    users = f.read().strip().split("\n")

# with docker
with NitterDockerContainer(host="0.0.0.0", port=8008) as nitter:
    for user in users:
        for idx, tweet in enumerate(get_tweets(user, pages=100, address=nitter.address)):
            print()
            pprint(tweet.dict())
            print(tweet.json(indent=4))


# with nitter.net
for user in users:
    for idx, tweet in enumerate(get_tweets(user, pages=100)):
        print()
        pprint(tweet.dict())
        print(tweet.json(indent=4))
