from nitter_scraper.profile import (
    html_parser,
    parse_user_id_from_banner,
    profile_parser,
    stat_cleaner,
    username_cleaner,
)
import pytest
from pytest_regressions import data_regression  # noqa: F401

from .common import profile_page_fixture  # noqa: F401


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


def test_parse_user_id_from_banner():
    before = "/pic/profile_banners%2F2474416796%2F1600567028%2F1500x500 "
    after = parse_user_id_from_banner(before)
    target = "2474416796"
    assert after == target


def test_html_parser(data_regression, profile_page_fixture):  # noqa: F811
    elements = html_parser(profile_page_fixture)
    results = {k: v.text for k, v in elements.items()}
    data_regression.check(results)


def test_profile_parser(data_regression, profile_page_fixture):  # noqa: F811
    elements = html_parser(profile_page_fixture)
    results = profile_parser(elements)
    data_regression.check(results)
