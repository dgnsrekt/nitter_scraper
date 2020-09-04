from pathlib import Path
from nitter_scraper import get_profile
from pprint import pprint
import json

root_dir = Path(__file__).parent
user_path = root_dir / "example.txt"

with open(user_path, mode="r") as f:
    users = f.read().strip().split("\n")

for user in users:
    profile = get_profile(user, not_found_ok=True)

    if profile:
        print(user)
        print(profile)
        pprint(profile.to_dict())
        pprint(profile.to_tuple())
        print(profile.to_json(indent=4))
