from typing import Dict, Optional

from requests_html import HTML, HTMLSession

from nitter_scraper.schema import Profile  # noqa: I100, I202


def username_cleaner(username: str) -> str:
    """Strips @ symbol from a username.

    Example:
        @dgnsrekt -> dgnsrekt

    Args:
        username: username with @ symbol to remove.

    Returns:
        Username with @ symbol stripped.
    """
    return username.replace("@", "")


def link_parser(element: HTML) -> str:
    """Gets the first link from an html element

    Used for the profiles website, photo and banner links.

    Args:
        element: HTML element with a link to parse.

    Returns:
        First link from a collection of links.
    """
    return list(element.links)[0]


def parse_user_id_from_banner(banner_url: str) -> str:
    """Parses the users id from the users banner photo url.

    The user id can only be parsed from the banner photos url.

    Example:
    ```
        /pic/profile_banners%2F2474416796%2F1600567028%2F1500x500 -> 2474416796
                               ^        ^
                               |        |
                               ----------
                               user id section in banner link
    ```

    Args:
        banner_url: URL of the profiles banner photo.

    Returns:
        The target profiles user id.

    """
    return banner_url.split("%2F")[1]


def stat_cleaner(stat: str) -> int:
    """Cleans and converts single stat.

    Used for the tweets, followers, following, and likes count sections.

    Args:
        stat: Stat to be cleaned.

    Returns:
        A stat with commas removed and converted to int.

    """
    return int(stat.replace(",", ""))


def profile_parser(elements: Dict) -> Dict:
    """Converts parsed sections to text.

    Cleans and processes a dictionary of gathered html elements.

    Args:
        elements: Elements prepared to clean and convert.

    Returns:
        A dictionary of element sections cleaned and converted to their finalized types.

    """
    elements["username"] = username_cleaner(elements["username"].text)

    elements["name"] = elements["name"].text

    if elements.get("location"):
        elements["location"] = elements["location"].text

    elements["is_verified"] = True if elements.get("is_verified") else False

    if elements.get("biography"):
        elements["biography"] = elements["biography"].text

    if elements.get("website"):
        elements["website"] = link_parser(elements["website"])

    if elements.get("profile_photo"):
        elements["profile_photo"] = link_parser(elements["profile_photo"])

    if elements.get("banner_photo"):
        elements["banner_photo"] = link_parser(elements["banner_photo"])
        elements["user_id"] = parse_user_id_from_banner(elements["banner_photo"])

    if elements.get("tweets_count"):
        elements["tweets_count"] = stat_cleaner(elements["tweets_count"].text)

    if elements.get("following_count"):
        elements["following_count"] = stat_cleaner(elements["following_count"].text)

    if elements.get("followers_count"):
        elements["followers_count"] = stat_cleaner(elements["followers_count"].text)

    if elements.get("likes_count"):
        elements["likes_count"] = stat_cleaner(elements["likes_count"].text)

    return elements


def html_parser(html: HTML) -> Dict:
    """Parses HTML element into individual sections

    Given an html element the html_parser will search for each profile section using
    CSS selectors. All parsed html elements are gathered into a dictionary and returned.

    Args:
        html: HTML element from a successful nitter profile scraped response.

    Returns:
        A dictionary of found elements from the parsed sections.

    """
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


def get_profile(
    username: str, not_found_ok: bool = False, address: str = "https://nitter.net"
) -> Optional[Profile]:
    """Scrapes nitter for the target users profile information.

    Args:
        username: The target profiles username.
        not_found_ok: If not_found_ok is false (the default), a ValueError is raised if the target
            profile doesn't exist. If not_found_ok is true, None will be returned instead.
        address: The address to scrape profile data from. The default scrape location is
            'https://nitter.net' which should be used as a backup. This value will normally be
            replaced by the address of a local docker container instance of nitter.

    Returns:
        Profile object if successfully scraped, otherwise None.

    Raises:
        ValueError: If the target profile does not exist and the not_found_ok argument is false.


    """
    url = f"{address}/{username}"
    session = HTMLSession()
    response = session.get(url)

    if response.status_code == 200:  # user exists
        elements = html_parser(response.html)
        parsed_elements = profile_parser(elements)
        return Profile.from_dict(parsed_elements)

    if not_found_ok:
        return None

    else:
        raise ValueError(f'Oops! Either "{username}" does not exist or is private.')
