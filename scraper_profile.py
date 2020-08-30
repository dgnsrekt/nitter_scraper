from requests_html import HTMLSession, HTML
import time
from pprint import pprint
from pathlib import Path

root_dir = Path(__file__).parent
user_path = root_dir / "users.txt"
print("exists:", root_dir.exists())

with open(user_path, mode="r") as f:
    users = f.read().strip().split("\n")
URL = "http://localhost:8080"


def get_location(user):
    url = URL + f"/{user}"
    session = HTMLSession()
    resp = session.get(url)
    html = resp.html
    print(user)
    try:
        x = html.find(".profile-location")[0].text
        print(x)
    except:
        pass


user = "dgnsrekt"
url = URL + f"/{user}"
session = HTMLSession()
page = session.get(url)
if page.status_code == 200:
    print(user, "exists")
    html = HTML(html=page.text, url="bunk", default_encoding="utf-8")
    print("location:", html.find(".profile-location")[0].text)
    print("profile_picture:", list(html.find(".profile-card-avatar")[0].links)[0])
    print("banner_photo:", list(html.find(".profile-banner")[0].links)[0])
