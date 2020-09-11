# Nitter Scraper

This library is a work around for anyone who enjoyed the simplicity of the [twitter-scraper](https://github.com/bisguzar/twitter-scraper/) library and needs a quick replacement until it comes back up.  Nitter Scraper leverages running a docker container instance of [nitter](https://github.com/zedeus/nitter) to scrape tweets and profile information. I attempted to make the api work as closely as possible to the original [twitter-scraper](https://github.com/bisguzar/twitter-scraper/) to minimize refactoring of twitter scraping projects.

## Use Nitter Scraper with docker
If you have docker installed you can use the NitterScraper context manager. It takes care of running/destorying a local nitter docker container instance. If you don't have docker installed you can use the get_tweets and get_profile to scraping from https://www.nitter.net


## Basic Usage
```
from nitter_scraper import NitterScraper

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    profile = nitter.get_profile("dgnsrekt")
    print(profile.json(indent=4))

```
#### Output
```
2020-09-11 10:11:08.533 | INFO     | nitter_scraper.nitter:get_client:35 - Docker connection successful.
2020-09-11 10:11:10.227 | INFO     | nitter_scraper.nitter:start:102 - Running container admiring_panini 368437c322.
{
    "username": "DGNSREKT",
    "name": "DGNSREKT",
    "profile_photo": "/pic/profile_images%2F1304387984440152064%2FiWh8NV8M.png",
    "tweets_count": 2897,
    "following_count": 905,
    "followers_count": 119,
    "likes_count": 4994,
    "is_verified": false,
    "banner_photo": "/pic/profile_banners%2F2474416796%2F1599825305%2F1500x500",
    "biography": "BITCOIN IS DEAD AGAIN. :(",
    "user_id": 2474416796,
    "location": "Moon",
    "website": "https://github.com/dgnsrekt"
}
2020-09-11 10:11:11.007 | INFO     | nitter_scraper.nitter:stop:105 - Stopping container admiring_panini 368437c322.
2020-09-11 10:11:16.346 | INFO     | nitter_scraper.nitter:stop:108 - Container admiring_panini 368437c322 Destroyed.


```

## Prerequisites

* Docker
* Python ^3.7

## Install
```
pip install nitter-scraper
```

## Examples
#### Scrape Users Tweets
```
from nitter_scraper import get_tweets
from nitter_scraper import NitterScraper

from pprint import pprint

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
    for tweet in get_tweets(user, pages=2):
        print()
        pprint(tweet.dict())
        print(tweet.json(indent=4))
```

#### Scrape User Profiles
```
from nitter_scraper import NitterScraper
from nitter_scraper import get_profile

from pprint import pprint

users = ["dgnsrekt"]

print("Scraping with local nitter docker instance.")

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    for user in users:
        profile = nitter.get_profile(user, not_found_ok=True)
        print(profile)
        pprint(profile.dict())
        print(profile.json(indent=4))


print("Scraping from https://www.nitter.net.")

for user in users:
    profile = get_profile(user, not_found_ok=True)
    print(profile)
    pprint(profile.dict())
    print(profile.json(indent=4))

```

## Profile & Tweet objects
The Profile and Tweet classes inherit from pydantic's BaseModel. This makes it easy to convert to a dict or json.
```
profile = get_profile("dgnsrekt")

profile.json(indent=4)

profile.dict()
```

### Profile Schema
These are the fields uses in the Profile class which is returned from the get_profile() method.
```
{
    "title": "Profile",
    "type": "object",
    "properties": {
        "username": {
            "title": "Username",
            "type": "string"
        },
        "name": {
            "title": "Name",
            "type": "string"
        },
        "profile_photo": {
            "title": "Profile Photo",
            "type": "string"
        },
        "tweets_count": {
            "title": "Tweets Count",
            "type": "integer"
        },
        "following_count": {
            "title": "Following Count",
            "type": "integer"
        },
        "followers_count": {
            "title": "Followers Count",
            "type": "integer"
        },
        "likes_count": {
            "title": "Likes Count",
            "type": "integer"
        },
        "is_verified": {
            "title": "Is Verified",
            "type": "boolean"
        },
        "banner_photo": {
            "title": "Banner Photo",
            "type": "string"
        },
        "biography": {
            "title": "Biography",
            "type": "string"
        },
        "user_id": {
            "title": "User Id",
            "type": "integer"
        },
        "location": {
            "title": "Location",
            "type": "string"
        },
        "website": {
            "title": "Website",
            "type": "string"
        }
    },
    "required": [
        "username",
        "name",
        "profile_photo",
        "tweets_count",
        "following_count",
        "followers_count",
        "likes_count",
        "is_verified"
    ]
}


```

### Tweet Schema
These are the fields uses in the Tweet class which is returned from the get_tweets() method.

```
{
    "title": "Tweet",
    "type": "object",
    "properties": {
        "tweet_id": {
            "title": "Tweet Id",
            "type": "integer"
        },
        "tweet_url": {
            "title": "Tweet Url",
            "type": "string"
        },
        "username": {
            "title": "Username",
            "type": "string"
        },
        "is_retweet": {
            "title": "Is Retweet",
            "type": "boolean"
        },
        "is_pinned": {
            "title": "Is Pinned",
            "type": "boolean"
        },
        "time": {
            "title": "Time",
            "type": "string",
            "format": "date-time"
        },
        "text": {
            "title": "Text",
            "type": "string"
        },
        "replies": {
            "title": "Replies",
            "type": "integer"
        },
        "retweets": {
            "title": "Retweets",
            "type": "integer"
        },
        "likes": {
            "title": "Likes",
            "type": "integer"
        },
        "entries": {
            "$ref": "#/definitions/Entries"
        }
    },
    "required": [
        "tweet_id",
        "tweet_url",
        "username",
        "is_retweet",
        "is_pinned",
        "time",
        "text",
        "replies",
        "retweets",
        "likes",
        "entries"
    ],
    "definitions": {
        "Entries": {
            "title": "Entries",
            "type": "object",
            "properties": {
                "hashtags": {
                    "title": "Hashtags",
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "cashtags": {
                    "title": "Cashtags",
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "urls": {
                    "title": "Urls",
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "photos": {
                    "title": "Photos",
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "videos": {
                    "title": "Videos",
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": [
                "hashtags",
                "cashtags",
                "urls",
                "photos",
                "videos"
            ]
        }
    }
}

```


## Limitation

* So far i've been able to pull about 800 tweets per user without issue.
* Unable to implement a way to scrape trends.
* birthday and is_private are not implemented in the profile.
* If the user does not have a banner the user_id cannot be scraped.
* The user_id cannot be scraped from tweets.

More docs coming soon.

## TODO
* Explain args
* More tests

## Contact Information
Telegram = Twitter = Tradingview = Discord = @dgnsrekt

Email = dgnsrekt@pm.me
