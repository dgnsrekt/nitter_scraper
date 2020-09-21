from pathlib import Path

SOURCE_ROOT = Path(__file__).parent
"""* A path to the nitter_scraper source code directory."""

PROJECT_ROOT = SOURCE_ROOT.parent
"""* A path to the nitter_scraper project directory."""

TEMPLATES_DIRECTORY = SOURCE_ROOT / "templates"
"""* A path to the template directory. The template is used by
jinja2 to render docker config files."""

TEST_DIRECTORY = PROJECT_ROOT / "tests"
"""* A path to the nitter_scraper test directory"""
