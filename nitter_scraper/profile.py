from requests_html import HTMLSession, HTML
from nitter_scraper.schema import Profile


def username_cleaner(username):
    return username.replace("@", "")


def link_parser(element):
    return list(element.links)[0]


def parse_user_id_from_banner_url(banner_url):
    return banner_url.split("%2F")[1]


def stat_cleaner(stat):
    return int(stat.replace(",", ""))


def profile_parser(elements):
    elements["username"] = username_cleaner(elements["username"].text)

    elements["name"] = elements["name"].text

    if elements.get("location"):
        elements["location"] = elements["location"].text

    if elements.get("is_verified"):
        elements["is_verified"] = True
    else:
        elements["is_verified"] = False

    if elements.get("biography"):
        elements["biography"] = elements["biography"].text

    if elements.get("website"):
        elements["website"] = link_parser(elements["website"])

    if elements.get("profile_photo"):
        elements["profile_photo"] = link_parser(elements["profile_photo"])

    if elements.get("banner_photo"):
        elements["banner_photo"] = link_parser(elements["banner_photo"])
        elements["user_id"] = parse_user_id_from_banner_url(elements["banner_photo"])

    if elements.get("tweets_count"):
        elements["tweets_count"] = stat_cleaner(elements["tweets_count"].text)

    if elements.get("following_count"):
        elements["following_count"] = stat_cleaner(elements["following_count"].text)

    if elements.get("followers_count"):
        elements["followers_count"] = stat_cleaner(elements["followers_count"].text)

    if elements.get("likes_count"):
        elements["likes_count"] = stat_cleaner(elements["likes_count"].text)

    return Profile.from_dict(elements)


def element_parser(html):
    elements = {}

    elements["username"] = html.find(".profile-card-username", first=True)

    elements["name"] = html.find(".profile-card-fullname", first=True)

    elements["biography"] = html.find(".profile-bio", first=True)

    elements["location"] = html.find(".profile-location", first=True)

    elements["is_verified"] = html.find(
        ".profile-card-fullname .icon-container .verified-icon", first=True
    )

    elements["profile_photo"] = html.find(".profile-card-avatar", first=True)

    elements["banner_photo"] = html.find(".profile-banner a", first=True)

    elements["website"] = html.find(".profile-website", first=True)

    profile_statlist = html.find(".profile-statlist", first=True)

    elements["tweets_count"] = profile_statlist.find(".posts .profile-stat-num", first=True)

    elements["following_count"] = profile_statlist.find(".following .profile-stat-num", first=True)

    elements["followers_count"] = profile_statlist.find(".followers .profile-stat-num", first=True)

    elements["likes_count"] = profile_statlist.find(".likes .profile-stat-num", first=True)

    elements = {k: v for k, v in elements.items() if v is not None}

    return elements


def get_profile(user: str, not_found_ok: bool = False, address="https://nitter.net"):
    url = f"{address}/{user}"
    session = HTMLSession()
    response = session.get(url)

    if response.status_code == 200:  # user exists

        elements = element_parser(response.html)

        return profile_parser(elements)

    if not_found_ok:
        return None

    else:
        raise ValueError(f'Oops! Either "{user}" does not exist or is private.')
