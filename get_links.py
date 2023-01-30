from requests import Session
from bs4 import BeautifulSoup
import re
import json


def get_credentials():
    f = open("login.json")
    json_file = json.load(f)
    return json_file



def get_course_links():
    with Session() as s:
        site = s.get("https://mescours.modestycouture.com/mon-compte/")
        login_crednetials = {"username": "helene.maurice", "password": "LGGmbp2022", "woocommerce-login-nonce": "5686106583", "_wp_http_referer": "/mon-compte/", "login": "Identification"}
        s.post("https://mescours.modestycouture.com/mon-compte/", login_crednetials)
        home_page = s.get("https://mescours.modestycouture.com/espace-membre/formation-modesty-couture-class/").content.decode('utf-8')
        soup = BeautifulSoup(home_page, "html.parser")
        print(home_page)
        # Get all the links in the page
        list = []
        for link in soup.find_all('a'):
            list.append(link.get('href'))

        course_list = []
        for i in range(len(list)):
            if re.search("^https://mescours.modestycouture.com/course/|^https://mescours.modestycouture.com/module/", list[i]):
                course_list.append(list[i])

        # The fisrt link of the list is: "Reprendre le cours"
        course_list.remove(course_list[0])

        # Write links in file
        f = open('links.txt', 'w')
        for line in range(len(course_list)):
            f.write(f"{course_list[line]}\n")


def get_file_links():
    # Get the links of the file
    file_list = []
    with open('links.txt') as links:
        for line in links:
            file_list.append(line)

    links_list = []
    for item in file_list:
        links_list.append(item.replace("\n", ""))

    return links_list



def get_vimeo_links():
    course_links = get_file_links()
    print(get_credentials())

    with Session() as session:
        session.post("https://mescours.modestycouture.com/mon-compte/", get_credentials())
        # Now open the first course link if it is a course link
        first_vimeo_link = course_links[34]
        course_page = session.get(first_vimeo_link).content.decode('utf-8')

        # create Soup object
        soup = BeautifulSoup(course_page, "html.parser")
        list = []
        for link in soup.find_all('iframe'):
            list.append(link.get('data-src'))

        vimeo_list = []
        for i in range(len(list)):
            if re.search("^https://player.vimeo.com/video/",
                         list[i]):
                vimeo_list.append(list[i])
        print(vimeo_list)


get_vimeo_links()