from nitter_scraper import NitterScraper
from nitter_scraper import get_profile

from pprint import pprint

users = ["dgnsrekt"]

print("Scraping with local nitter docker instance.")

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    for user in users:
        profile = nitter.get_profile(user, not_found_ok=True)
        print(profile)
        pprint(profile.dict())
        print(profile.json(indent=4))


print("Scraping from https://www.nitter.net.")

for user in users:
    profile = get_profile(user, not_found_ok=True)
    print(profile)
    pprint(profile.dict())
    print(profile.json(indent=4))
