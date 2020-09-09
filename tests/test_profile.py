import pytest
from pytest_regressions import data_regression

from nitter_scraper.paths import TEST_DIRECTORY
from nitter_scraper.profile import element_parser, profile_parser
from .common import profile_page_fixture


def test_element_parser(data_regression, profile_page_fixture):
    elements = element_parser(profile_page_fixture)
    results = {k: v.text for k, v in elements.items()}
    data_regression.check(results)


def test_profile_parser(data_regression, profile_page_fixture):
    elements = element_parser(profile_page_fixture)
    results = profile_parser(elements).json()
    data_regression.check(results)
