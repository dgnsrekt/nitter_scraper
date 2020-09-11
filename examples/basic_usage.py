from nitter_scraper import NitterDockerContainer, get_profile

with NitterDockerContainer(host="0.0.0.0", port=8008) as nitter:
    profile = nitter.get_profile("dgnsrekt")
    print(profile.json(indent=4))
