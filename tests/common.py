from nitter_scraper.paths import TEST_DIRECTORY
import pytest
from requests_html import HTML

URL = "https://www.nitter.net"
USERNAME = "dgnsrekt"
ADDRESS = f"{URL}/{USERNAME}"


@pytest.fixture
def profile_page_fixture():
    test_page_path = TEST_DIRECTORY / "testpage.html"

    assert test_page_path.exists()

    with open(test_page_path, mode="r") as file:
        html = HTML(html=file.read(), url=ADDRESS, default_encoding="utf-8")
    return html
