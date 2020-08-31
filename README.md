# Nitter Scraper

This library is a work around for anyone who enjoyed the simplicity of the [twitter-scraper](https://github.com/bisguzar/twitter-scraper/) library and needs a quick replacement until it comes back up.  Nitter Scraper leverages running a docker instance of [nitter](https://github.com/zedeus/nitter) to scrape tweets and profile information. I attempted to make the api work as closely as possible to the original to minimize refactoring of other projects.

## Known Issues

* Unable to implement a way to scrape trends.
* birthday and is_private are not implemented in the profile.
* If the user does not have a banner the user_id cannot be scraped.
* The user_id cannot be scraped from tweets.
* Tweet entries have not been implemented yet.

## Prerequisites

* Docker
* Docker-compose
* Python ^3.7

## How to run the examples.
```
git clone git@github.com:dgnsrekt/nitter_scraper.git
cd nitter_scraper
docker-compose up -d
poetry install
poetry shell
```
Add twitter usernames to the example.txt delimited by newlines.

Run profile scraping example
```
python3 example_profile.py
```
Run tweet scraping example
```
python3 example_tweet.py
```

More docs coming soon.

## Contact Information
Telegram = Twitter = Tradingview = Discord = @dgnsrekt

Email = dgnsrekt@pm.me
