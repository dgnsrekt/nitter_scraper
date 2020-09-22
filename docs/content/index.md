# Nitter Scraper

Nitter Scraper is for anyone who enjoys the [twitter-scraper](https://github.com/bisguzar/twitter-scraper/) library. Nitter Scraper leverages running a local docker container instance of [nitter](https://github.com/zedeus/nitter) to scrape a users tweets and profile information without the twitter api ratelimit. This api works similar to the [twitter-scraper](https://github.com/bisguzar/twitter-scraper/) project with a few differences.

## Docker Engine
For the best experience use this library with [Docker Engine](https://docs.docker.com/engine/) properly installed. The NitterScraper manager will start, stop and remove a docker instance of [nitter](https://hub.docker.com/r/zedeus/nitter). If you can't run docker you can import the get_tweets and get_profile functions to scrape from [nitter.net](http://www.nitter.net).


## Getting Started

### Prereqs
* Docker Engine
* Python ^3.7

### Install
```shell
pip install nitter-scraper
```

#### How to Scrape a twitter users profile information.
```python
from pprint import pprint

from nitter_scraper import NitterScraper

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    profile = nitter.get_profile("dgnsrekt")
    print("serialize to json\n")
    print(profile.json(indent=4))
    print("serialize to a dictionary\n")
    pprint(profile.dict())

```
#### Output
```python
$ python3 examples/basic_usage.py
2020-09-21 18:11:23.429 | INFO     | nitter_scraper.nitter:_get_client:31 - Docker connection successful.
2020-09-21 18:11:25.102 | INFO     | nitter_scraper.nitter:start:135 - Running container infallible_noyce 91122c9b7b.
serialize to json

{
    "username": "DGNSREKT",
    "name": "DGNSREKT",
    "profile_photo": "/pic/profile_images%2F1307990704384245760%2FSBVd3XT6.png",
    "tweets_count": 2897,
    "following_count": 904,
    "followers_count": 117,
    "likes_count": 4992,
    "is_verified": false,
    "banner_photo": "/pic/profile_banners%2F2474416796%2F1600684261%2F1500x500",
    "biography": "BITCOIN IS DEAD AGAIN. :(",
    "user_id": 2474416796,
    "location": "Moon",
    "website": "https://github.com/dgnsrekt"
}
serialize to a dictionary

{'banner_photo': '/pic/profile_banners%2F2474416796%2F1600684261%2F1500x500',
 'biography': 'BITCOIN IS DEAD AGAIN. :(',
 'followers_count': 117,
 'following_count': 904,
 'is_verified': False,
 'likes_count': 4992,
 'location': 'Moon',
 'name': 'DGNSREKT',
 'profile_photo': '/pic/profile_images%2F1307990704384245760%2FSBVd3XT6.png',
 'tweets_count': 2897,
 'user_id': 2474416796,
 'username': 'DGNSREKT',
 'website': 'https://github.com/dgnsrekt'}
2020-09-21 18:11:25.905 | INFO     | nitter_scraper.nitter:stop:139 - Stopping container infallible_noyce 91122c9b7b.
2020-09-21 18:11:31.284 | INFO     | nitter_scraper.nitter:stop:142 - Container infallible_noyce 91122c9b7b Destroyed.


```
#### Next step run the [examples](https://nitter-scraper.readthedocs.io/en/latest/examples/)

## NitterScraper Limitation

* About max 800 tweets per user.
* Unable to scrape trends from nitter.
* To scrape the user_id the user must have a banner photo. If the banner photo url isn't present
the user_id will be none.
* The user_id cannot be scraped from the tweets.
* birthday and is_private are not implemented in the profile.

## Contact Information
Telegram = Twitter = Tradingview = Discord = @dgnsrekt

Email = dgnsrekt@pm.me
