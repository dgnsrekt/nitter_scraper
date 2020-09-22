from nitter_scraper.paths import TEST_DIRECTORY
from nitter_scraper.tweets import pagination_parser, parse_tweet, timeline_parser
import pytest
from pytest_regressions import data_regression  # noqa: F401

from .common import ADDRESS, profile_page_fixture, URL, USERNAME  # noqa: F401


@pytest.fixture
def timeline_items_fixtures(profile_page_fixture):  # noqa: F811
    timeline = timeline_parser(profile_page_fixture)
    return [item for item in timeline.find(".timeline-item")]


def test_timeline_parser(profile_page_fixture):  # noqa: F811
    with open(TEST_DIRECTORY / "timeline_output.txt") as file:
        target = file.read().strip().split("\n")

    output = timeline_parser(profile_page_fixture).text.split("\n")
    assert output == target


def test_pagination_parser(profile_page_fixture):  # noqa: F811
    timeline = timeline_parser(profile_page_fixture)
    output = pagination_parser(timeline, URL, USERNAME)
    target = f"{ADDRESS}?cursor=HBaCwL7dmvLIuSMAAA%3D%3D"
    assert output == target


@pytest.mark.parametrize("index", [i for i in range(0, 20)])
def test_parse_tweets(data_regression, timeline_items_fixtures, index):  # noqa: F811
    results = parse_tweet(timeline_items_fixtures[index])
    data_regression.check(results)
