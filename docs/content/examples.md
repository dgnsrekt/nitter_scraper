# Examples

### How to scrape a users Tweets.
```python
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
```

### How to scrape a users profiles.
```python
from pprint import pprint

import nitter_scraper
from nitter_scraper import NitterScraper

users = ["dgnsrekt"]

print("Scraping with local nitter docker instance.")

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    for user in users:
        profile = nitter.get_profile(user, not_found_ok=True)
        if profile:
            print(profile)
            pprint(profile.dict())
            print(profile.json(indent=4))


print("Scraping from https://www.nitter.net.")

for user in users:
    profile = nitter_scraper.get_profile(user, not_found_ok=True)
    if profile:
        print(profile)
        pprint(profile.dict())
        print(profile.json(indent=4))

```

### How to scrape tweets related to hashtag or cashtag.
```python
from pprint import pprint

import nitter_scraper
from nitter_scraper import NitterScraper

queries = ["#ToTheMoon", "$USDT"]

print("Scraping with local nitter docker instance.")

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    for query in queries:
        for tweet in nitter.get_tweets(query, pages=2):
            print()
            pprint(tweet.dict())
            print(tweet.json(indent=4))

print("Scraping from https://www.nitter.net.")

for query in queries:
    for tweet in nitter.get_tweets(query, pages=2):
        print()
        pprint(tweet.dict())
        print(tweet.json(indent=4))

```

### How to poll a users profile for the latest tweet.
```python
import time

from nitter_scraper import NitterScraper

last_tweet_id = None

with NitterScraper(port=8008) as nitter:
    while True:
        for tweet in nitter.get_tweets("dgnsrekt", pages=1, break_on_tweet_id=last_tweet_id):

            if tweet.is_pinned is True:
                continue

            if tweet.is_retweet is True:
                continue

            if tweet.tweet_id != last_tweet_id:
                print(tweet.json(indent=4))

            last_tweet_id = tweet.tweet_id

            break

        time.sleep(0.1)

```
