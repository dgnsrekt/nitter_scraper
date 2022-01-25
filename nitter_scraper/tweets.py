"""Module for scraping tweets"""
#from datetime import datetime
from dateutil import parser as dateparser
import re
from typing import Dict, Optional

from requests_html import HTMLSession

from nitter_scraper.schema import Tweet  # noqa: I100, I202
from nitter_scraper.schema import Card


def link_parser(tweet_link):
    links = list(tweet_link.links)
    tweet_url = links[0]
    parts = links[0].split("/")

    tweet_id = parts[-1].replace("#m", "")
    username = parts[1]
    return tweet_id, username, tweet_url


def date_parser(tweet_date):
    return dateparser.parse(tweet_date.replace('·', ''))


def clean_stat(stat):
    return int(stat.replace(",", ""))


def stats_parser(tweet_stats):
    stats = {}
    for ic in tweet_stats.find(".icon-container"):
        key = ic.find("span", first=True).attrs["class"][0].replace("icon", "").replace("-", "")
        value = ic.text
        stats[key] = value
    return stats


def attachment_parser(attachements):
    photos, videos = [], []
    if attachements:
        photos = [i.attrs["src"] for i in attachements.find("img")]
        videos = [i.attrs["src"] for i in attachements.find("source")]
    return photos, videos


def cashtag_parser(text):
    cashtag_regex = re.compile(r"\$[^\d\s]\w*")
    return cashtag_regex.findall(text)


def hashtag_parser(text):
    hashtag_regex = re.compile(r"\#[^\d\s]\w*")
    return hashtag_regex.findall(text)


def url_parser(links):
    return sorted(filter(lambda link: "http://" in link or "https://" in link, links))


def parse_tweet(html) -> Dict:
    data = {}
    id, username, url = link_parser(html.find(".tweet-link", first=True))
    data["tweet_id"] = id
    data["tweet_url"] = url
    data["username"] = username

    retweet = html.find(".retweet-header .icon-container .icon-retweet", first=True)
    data["is_retweet"] = True if retweet else False

    body = html.find(".tweet-body", first=True)

    pinned = body.find(".pinned", first=True)
    data["is_pinned"] = True if pinned is not None else False

    data["time"] = date_parser(body.find(".tweet-date a", first=True).attrs["title"])

    content = body.find(".tweet-content", first=True)
    data["text"] = content.text

    # tweet_header = html.find(".tweet-header") #NOTE: Maybe useful later on
    
    card = html.find("div.card.large", first=True)
    
    if card:
        data["card"] = {}
        card_title = card.find(".card-title", first=True)
        if card_title:
            data["card"]["title"] = card_title.text
        card_description = card.find(".card-description", first=True)
        if card_description:
            data["card"]["description"] = card_description.text
        
        card_image = card.find(".card-image img", first=True)
        if card_image:
            data["card"]["image"] = card_image.attrs["src"]
            
        data["card"] = Card.from_dict(data["card"])
    else:
        data["card"] = None
        
    
    stats = stats_parser(html.find(".tweet-stats", first=True))

    data["replies"] = clean_stat(stats.get("comment")) if stats.get("comment") else 0

    data["retweets"] = clean_stat(stats.get("retweet"))if stats.get("retweet") else 0

    data["likes"] = clean_stat(stats.get("heart")) if stats.get("heart") else 0

    entries = {}
    entries["hashtags"] = hashtag_parser(content.text)
    entries["cashtags"] = cashtag_parser(content.text)
    entries["urls"] = url_parser(content.links)

    photos, videos = attachment_parser(body.find(".attachments", first=True))
    entries["photos"] = photos
    entries["videos"] = videos

    data["entries"] = entries
    # quote = html.find(".quote", first=True) #NOTE: Maybe useful later on
    return data


def timeline_parser(html):
    return html.find(".timeline", first=True)


def pagination_parser(timeline, address, username) -> str:
    next_page = list(timeline.find(".show-more")[-1].links)[0]
    return f"{address}/{username}/search{next_page}"

def get_tweets(
    username: str,
    pages: int = 25,
    break_on_tweet_id: Optional[int] = None,
    address="https://nitter.net",
    headers: Optional[dict[str, str]] = None,
    params: Optional[dict[str, str]] = None,
    proxies: Optional[dict[str, str]] = None,
) -> Tweet:
    """Gets the target users tweets

    Args:
        username: Targeted users username.
        pages: Max number of pages to lookback starting from the latest tweet.
        break_on_tweet_id: Gives the ability to break out of a loop if a tweets id is found.
        address: The address to scrape from. The default is https://nitter.net which should
            be used as a fallback address. Refer to https://github.com/zedeus/nitter/wiki/Instances
            for a list of instances.
        headers: HTTP headers to be passed.
        params: Search query parameters as found in Nitter URLs upon search.
        proxies: Passed to HTMLSession.get().

    Yields:
        Tweet Objects

    """
    url = f"{address}/{username}/search"
    session = HTMLSession()
    
    if headers:
        session.headers.update(headers)

    def gen_tweets(pages):
        response = session.get(url, params=params, proxies=proxies)

        while pages > 0:
            if response.status_code == 200:
                timeline = timeline_parser(response.html)

                next_url = pagination_parser(timeline, address, username)

                timeline_items = timeline.find(".timeline-item")

                for item in timeline_items:
                    if "show-more" in item.attrs["class"]:
                        continue

                    tweet_data = parse_tweet(item)
                    tweet = Tweet.from_dict(tweet_data)

                    if tweet.tweet_id == break_on_tweet_id:
                        pages = 0
                        break

                    yield tweet

                response = session.get(next_url, params=params, proxies=proxies)
            else:
                #print(f'Response status code: {response.status_code}')
                #last_error_html = response.html
                pages = 0
                break
            pages -= 1

    yield from gen_tweets(pages)
