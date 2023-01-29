from requests import Session
from bs4 import BeautifulSoup

with Session() as s:
    site = s.get("https://mescours.modestycouture.com/mon-compte/")
    login_crednetials = {"username": "helene.maurice", "password": "LGGmbp2022", "woocommerce-login-nonce": "5686106583", "_wp_http_referer": "/mon-compte/", "login": "Identification"}
    s.post("https://mescours.modestycouture.com/mon-compte/", login_crednetials)
    home_page = s.get("https://mescours.modestycouture.com/mon-compte/")
    print(home_page.content.decode('utf-8'))
