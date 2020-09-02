from requests_html import HTMLSession, HTML
import re
from datetime import datetime
from nitter_scraper.schema import Tweet
from nitter_scraper.config import NITTER_URL

session = HTMLSession()


def parse_tweet_link(tweet_link):
    links = list(tweet_link.links)
    tweet_url = links[0]
    parts = links[0].split("/")

    tweet_id = parts[-1].replace("#m", "")
    username = parts[1]
    return tweet_id, username, tweet_url


def parse_date(tweet_date):
    split_datetime = tweet_date.split(",")

    day, month, year = split_datetime[0].strip().split("/")
    hours, minutes, seconds = split_datetime[1].strip().split(":")

    day = int(day)
    month = int(month)
    year = int(year)

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    return datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)


def clean_stat(stat):
    return int(stat.replace(",", ""))


def parse_stats(tweet_stats):
    stats = {}
    for ic in tweet_stats.find(".icon-container"):
        key = ic.find("span", first=True).attrs["class"][0].replace("icon", "").replace("-", "")
        value = ic.text
        stats[key] = value
    return stats


def parse_attachments(attachements):
    photos, videos = [], []
    if attachements:
        photos = [i.attrs["src"] for i in attachements.find("img")]
        videos = [i.attrs["src"] for i in attachements.find("source")]
    return photos, videos


def parse_cashtags(text):
    cashtag_regex = re.compile(r"\$[^\d\s]\w*")
    matched = cashtag_regex.findall(text)
    return matched


def parse_hashtags(text):
    cashtag_regex = re.compile(r"\#[^\d\s]\w*")
    matched = cashtag_regex.findall(text)
    return matched


def parse_urls(links):
    links = list(filter(lambda link: "http://" in link or "https://" in link, links))
    return links


def parse_tweet(raw_tweet):
    data = {}
    tweet_id, username, tweet_url = parse_tweet_link(raw_tweet.find(".tweet-link", first=True))
    data["tweet_id"] = tweet_id
    data["tweet_url"] = tweet_url
    data["username"] = username

    retweet_header = raw_tweet.find(".retweet-header .icon-container .icon-retweet", first=True)
    retweet = True if retweet_header else False
    data["is_retweet"] = retweet

    body = raw_tweet.find(".tweet-body", first=True)
    pinned = True if body.find(".pinned", first=True) is not None else False
    data["is_pinned"] = pinned

    tweet_datetime = parse_date(body.find(".tweet-date a", first=True).attrs["title"])
    data["time"] = tweet_datetime

    text = body.find(".tweet-content", first=True)
    data["text"] = text.text

    # tweet_header = raw_tweet.find(".tweet-header") #NOTE: Maybe useful later on

    tweet_stats = parse_stats(raw_tweet.find(".tweet-stats", first=True))

    if tweet_stats.get("comment"):
        data["replies"] = clean_stat(tweet_stats.get("comment"))

    if tweet_stats.get("retweet"):
        data["retweets"] = clean_stat(tweet_stats.get("retweet"))

    if tweet_stats.get("heart"):
        data["likes"] = clean_stat(tweet_stats.get("heart"))

    entries = {}
    entries["hashtags"] = parse_hashtags(text.text)
    entries["cashtags"] = parse_cashtags(text.text)
    entries["urls"] = parse_urls(text.links)
    photos, videos = parse_attachments(body.find(".attachments", first=True))
    entries["photos"] = photos
    entries["videos"] = videos
    data["entries"] = entries
    # quote = raw_tweet.find(".quote", first=True) #NOTE: Maybe useful later on
    return Tweet(**data)


def get_tweets(query, pages=25, break_on_tweet_id: int = None):
    url = f"{NITTER_URL}/{query}"

    def gen_tweets(pages):
        response = session.get(url)

        while pages > 0:
            if response.status_code == 200:
                html = HTML(html=response.text, default_encoding="utf-8")
                timeline = html.find(".timeline", first=True)

                next_url = list(timeline.find(".show-more")[-1].links)[0]
                next_url = f"{NITTER_URL}/{query}{next_url}"

                timeline_items = timeline.find(".timeline-item")

                for item in timeline_items:
                    if "show-more" in item.attrs["class"]:
                        continue

                    tweet = parse_tweet(item)

                    if tweet.tweet_id == break_on_tweet_id:
                        pages = 0
                        break

                    yield tweet

            response = session.get(next_url)
            pages -= 1

    yield from gen_tweets(pages)
