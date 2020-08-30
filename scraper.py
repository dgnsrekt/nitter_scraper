from requests_html import HTMLSession, HTML
import time
from pprint import pprint
from pathlib import Path
import pendulum

root_dir = Path(__file__).parent
user_path = root_dir / "users.txt"
print("exists:", root_dir.exists())

with open(user_path, mode="r") as f:
    users = f.read().strip().split("\n")

BASE_URL = "http://localhost:8080"


def parse_stats(tweet):
    print("STATS")

    stats = tweet.find(".tweet-stats", first=True)

    icons_containers = stats.find(".icon-container")
    for i in icons_containers:
        print(
            i.find("span", first=True).attrs["class"][0].replace("icon", "").replace("-", ""),
            i.text,
        )


def parse_name(header):
    full_user_name = header.find(".fullname-and-username", first=True)
    fullname = full_user_name.find(".fullname", first=True)
    username = full_user_name.find(".username", first=True)
    print("name parser")
    print("fullname:", fullname)
    print("username:", username)


def parse_date(tweet_date):
    print("DATE PARSER")
    date = tweet_date.find("a", first=True).attrs["title"]
    date = date.replace(",", "")
    date = date.replace("/", "-")
    print(date)
    print(pendulum.parse(date, strict=False))


def parse_header(tweet):
    print("header")

    header = tweet.find(".tweet-header", first=True)

    tweet_name_row = header.find(".tweet-name-row", first=True)
    tweet_date = header.find(".tweet-date", first=True)

    parse_name(tweet_name_row)
    parse_date(tweet_date)


def parse_message_id(tweet_link):
    print("tweet_link:", tweet_link.attrs["href"])
    message_id = tweet_link.attrs["href"].split("/")[-1]
    message_id = message_id.strip("#m")
    print("message_id:", message_id)


def parse_tweet(el):
    print()
    print("TWEET START")
    # print(el.html)
    retweet = el.find(".retweet-header", first=True)
    body = el.find(".tweet-content", first=True)
    tweet_link = el.find(".tweet-link", first=True)
    parse_stats(el)
    parse_header(el)
    parse_message_id(tweet_link)

    print("body", body.text)
    print("body_atters", body.attrs)

    if retweet:
        print("found retweet")

    print("TWEET END")
    print()


def get_tweets(user, url=None, index=0, tweets_parsed=0):
    print("current url:", url)
    print("index:", index)
    print("tweets parsed:", tweets_parsed)
    if url is None:
        url = f"{BASE_URL}/{user}"

    print()
    print("url:", url)

    session = HTMLSession()
    page = session.get(url)

    if page.status_code == 200:
        print(user, "exists")
        html = HTML(html=page.text, url="bunk", default_encoding="utf-8")
        timeline = html.find(".timeline")[0]
        print(timeline)
        print("timeline", list(timeline.find(".show-more")[0].links))

        timeline_items = html.find(".timeline-item")
        for item in timeline_items:
            if "show-more" in item.attrs["class"]:
                continue
            parse_tweet(item)
            tweets_parsed += 1

        next_link = list(timeline.find(".show-more"))
        next_link = list(next_link[-1].links)[0]
        print("next:", next_link)
        next_url = f"{BASE_URL}/{user}{next_link}"
        print(next_url)

        if next_link:
            index += 1
            get_tweets(user, url=next_url, index=index, tweets_parsed=tweets_parsed)

        # print("location:", html.find(".profile-location")[0].text)
        # print("profile_picture:", list(html.find(".profile-card-avatar")[0].links)[0])
        # print("banner_photo:", list(html.find(".profile-banner")[0].links)[0])


for user in users:
    start = time.time()
    get_tweets(user)
    end = time.time()
    print("user:", user)
    print("took:", end - start)
    time.sleep(15)
