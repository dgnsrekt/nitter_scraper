from requests_html import HTMLSession, HTML
from nitter_scraper.schema import Profile
from nitter_scraper.config import NITTER_URL


def get_profile(user):
    url = f"{NITTER_URL}/{user}"
    session = HTMLSession()
    page = session.get(url)

    elements = {}
    if page.status_code == 200:  # user exists

        html = HTML(html=page.text, default_encoding="utf-8")

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

        elements["following_count"] = profile_statlist.find(
            ".following .profile-stat-num", first=True
        )

        elements["followers_count"] = profile_statlist.find(
            ".followers .profile-stat-num", first=True
        )
        elements["likes_count"] = profile_statlist.find(".likes .profile-stat-num", first=True)

        elements = {k: v for k, v in elements.items() if v is not None}

        return Profile.from_elements(elements)

    else:
        raise ValueError(f'Oops! Either "{name}" does not exist or is private.')
