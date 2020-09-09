from pathlib import Path
from nitter_scraper import NitterDockerContainer
from nitter_scraper import get_profile
from pprint import pprint
import json

root_dir = Path(__file__).parent
user_path = root_dir / "example_users.txt"

with open(user_path, mode="r") as f:
    users = f.read().strip().split("\n")

# with docker
profiles = []
with NitterDockerContainer(host="0.0.0.0", port=8008) as nitter:
    for user in users:
        profile = get_profile(user, not_found_ok=True, address=nitter.address)

        if profile:
            profiles.append(profile)

for profile in profiles:
    print(profile)
    pprint(profile.dict())
    print(profile.json(indent=4))


# with nitter.net
profiles = []
for user in users:
    profile = get_profile(user, not_found_ok=True)

    if profile:
        profiles.append(profile)

for profile in profiles:
    print(profile)
    pprint(profile.dict())
    print(profile.json(indent=4))
