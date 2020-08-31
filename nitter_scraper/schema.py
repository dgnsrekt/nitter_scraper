from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder
from datetime import datetime
import json

from typing import Optional, List
from pprint import pprint


@dataclass
class Entries:
    hashtags: List[str]
    cashtags: List[str]
    urls: List[str]
    photos: List[str]
    videos: List[str]


@dataclass
class Tweet:
    tweet_id: int
    tweet_url: str
    username: str
    # user_id: int
    is_retweet: bool
    is_pinned: bool
    time: datetime
    text: str
    replies: int
    retweets: int
    likes: int
    entries: Entries

    def json(self, indent=4):
        return json.dumps(self, indent=indent, default=pydantic_encoder)


@dataclass
class Profile:
    username: str
    name: str
    # birthday: str
    profile_photo: str
    tweets_count: int
    following_count: int
    followers_count: int
    likes_count: int
    is_verified: bool
    # is_private: bool

    banner_photo: Optional[str] = None
    biography: Optional[str] = None
    user_id: Optional[int] = None
    location: Optional[str] = None
    website: Optional[str] = None

    def json(self, indent=4):
        return json.dumps(self, indent=indent, default=pydantic_encoder)

    @classmethod
    def parse_url(cls, element):
        return list(element.links)[0]

    @classmethod
    def get_user_id_from_banner_url(cls, banner_url):
        return banner_url.split("%2F")[1]

    @classmethod
    def clean_stat(cls, stat):
        return int(stat.replace(",", ""))

    @classmethod
    def from_elements(cls, elements):
        elements["username"] = elements["username"].text

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
            elements["website"] = cls.parse_url(elements["website"])

        if elements.get("profile_photo"):
            elements["profile_photo"] = cls.parse_url(elements["profile_photo"])

        if elements.get("banner_photo"):
            elements["banner_photo"] = cls.parse_url(elements["banner_photo"])
            elements["user_id"] = cls.get_user_id_from_banner_url(elements["banner_photo"])

        if elements.get("tweets_count"):
            elements["tweets_count"] = cls.clean_stat(elements["tweets_count"].text)

        if elements.get("following_count"):
            elements["following_count"] = cls.clean_stat(elements["following_count"].text)

        if elements.get("followers_count"):
            elements["followers_count"] = cls.clean_stat(elements["followers_count"].text)

        if elements.get("likes_count"):
            elements["likes_count"] = cls.clean_stat(elements["likes_count"].text)

        return cls(**elements)
