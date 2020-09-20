import pytest
from pytest_regressions import data_regression

from nitter_scraper.paths import TEST_DIRECTORY
from nitter_scraper.profile import (
    element_parser,
    profile_parser,
    username_cleaner,
    parse_user_id_from_banner_url,
    stat_cleaner,
)
from .common import profile_page_fixture


@pytest.mark.parametrize(
    "before,target", [("2,898", 2898), ("904", 904), ("118", 118), ("4,993", 4993)]
)
def test_stat_cleaner(before, target):
    after = stat_cleaner(before)
    assert after == target


def test_username_cleaner():
    before = "@dgnsrekt"
    after = username_cleaner(before)
    target = "dgnsrekt"
    assert after == target


def test_parse_user_id_from_banner_url():
    before = "/pic/profile_banners%2F2474416796%2F1600567028%2F1500x500 "
    after = parse_user_id_from_banner_url(before)
    target = "2474416796"
    assert after == target


def test_element_parser(data_regression, profile_page_fixture):
    elements = element_parser(profile_page_fixture)
    results = {k: v.text for k, v in elements.items()}
    data_regression.check(results)


def test_profile_parser(data_regression, profile_page_fixture):
    elements = element_parser(profile_page_fixture)
    results = profile_parser(elements)
    data_regression.check(results)
