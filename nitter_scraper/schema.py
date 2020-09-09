from pydantic import BaseModel as Base
from dataclasses import asdict, astuple
from datetime import datetime
import json

from typing import Optional, List


class Entries(Base):
    hashtags: List[str]
    cashtags: List[str]
    urls: List[str]
    photos: List[str]
    videos: List[str]


class Tweet(Base):
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

    # def to_dict(self):
    # return asdict(self)

    # def to_json(self, indent=4):
    # return json.dumps(self, indent=indent, default=pydantic_encoder)

    # def to_tuple(self):
    # return astuple(self)

    @classmethod
    def from_dict(cls, elements):
        return cls(**elements)


class Profile(Base):
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

    # def to_dict(self):
    # return asdict(self)

    # def to_json(self, indent=4):
    # return json.dumps(self, indent=indent, default=pydantic_encoder)

    # def to_tuple(self):
    # return astuple(self)

    @classmethod
    def from_dict(cls, elements):
        return cls(**elements)
