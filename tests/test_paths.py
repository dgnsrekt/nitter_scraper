import tomlkit

import nitter_scraper
from nitter_scraper.paths import PROJECT_ROOT, SOURCE_ROOT


def test_sanity():
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    assert pyproject_path.exists()

    with open(pyproject_path, mode="r") as file:
        content = tomlkit.parse(file.read())

    assert content["tool"]["poetry"].get("version") is not None


def test_sanity_two():
    assert SOURCE_ROOT.exists()
