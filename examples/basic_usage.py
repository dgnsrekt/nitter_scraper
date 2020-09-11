from nitter_scraper import NitterScraper, get_profile

with NitterScraper(host="0.0.0.0", port=8008) as nitter:
    profile = nitter.get_profile("dgnsrekt")
    print(profile.json(indent=4))
