from pathlib import Path
from nitter_scraper import get_profile
from pprint import pprint
import json

root_dir = Path(__file__).parent
user_path = root_dir / "example.txt"

with open(user_path, mode="r") as f:
    users = f.read().strip().split("\n")

for user in users:
    profile = get_profile(user)
    print(user)
    print(profile)
    print(profile.json(indent=4))
