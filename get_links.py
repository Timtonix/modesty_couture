from requests import Session
from bs4 import BeautifulSoup
import re



with Session() as s:
    site = s.get("https://mescours.modestycouture.com/mon-compte/")
    login_crednetials = {"username": "helene.maurice", "password": "LGGmbp2022", "woocommerce-login-nonce": "5686106583", "_wp_http_referer": "/mon-compte/", "login": "Identification"}
    s.post("https://mescours.modestycouture.com/mon-compte/", login_crednetials)
    home_page = s.get("https://mescours.modestycouture.com/espace-membre/formation-modesty-couture-class/").content.decode('utf-8')
    soup = BeautifulSoup(home_page, "html.parser")

    # Get all the links in the page
    list = []
    for link in soup.find_all('a'):
        list.append(link.get('href'))

    course_list = []
    for i in range(len(list)):
        print(i)
        if re.search("^https://mescours.modestycouture.com/course/", list[i]):
            course_list.append(list[i])

    print(course_list)
