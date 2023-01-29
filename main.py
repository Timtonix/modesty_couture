from requests import Session
from bs4 import BeautifulSoup

links = open("links.html")
html_links = links.read()


with Session() as s:
    site = s.get("https://mescours.modestycouture.com/mon-compte/")
    login_crednetials = {"username": "helene.maurice", "password": "LGGmbp2022", "woocommerce-login-nonce": "5686106583", "_wp_http_referer": "/mon-compte/", "login": "Identification"}
    s.post("https://mescours.modestycouture.com/mon-compte/", login_crednetials)
    home_page = s.get("https://mescours.modestycouture.com/module/1-premieres-bases/")
    soup = BeautifulSoup(html_links, "html.parser")

