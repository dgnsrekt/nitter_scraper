from pprint import pprint

import nitter_scraper
from nitter_scraper import NitterScraper

users = ["dgnsrekt"]

print("Scraping with local nitter docker instance.")

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    for user in users:
        for tweet in nitter.get_tweets(user, pages=2):
            print()
            pprint(tweet.dict())
            print(tweet.json(indent=4))


print("Scraping from https://www.nitter.net.")

for user in users:
    for tweet in nitter_scraper.get_tweets(user, pages=2):
        print()
        pprint(tweet.dict())
        print(tweet.json(indent=4))
