from pathlib import Path
from nitter_scraper.profile import get_profile
from pprint import pprint
from pydantic.json import pydantic_encoder
import json

root_dir = Path(__file__).parent
user_path = root_dir / "users.txt"

with open(user_path, mode="r") as f:
    users = f.read().strip().split("\n")

for user in users:
    profile = get_profile(user)
    print(user)
    print(profile)
    print(json.dumps(profile, indent=4, default=pydantic_encoder))
