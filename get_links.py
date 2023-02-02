from requests import Session
from bs4 import BeautifulSoup
import re
import os
import json


def get_credentials():
    f = open("login.json")
    json_file = json.load(f)

    with Session() as s:
        site = s.get("https://mescours.modestycouture.com/mon-compte/").content.decode('utf-8')

        soup = BeautifulSoup(site, "html.parser")
        input_list = []
        for input_html in soup.find_all('input'):
            input_list.append(input_html.get('value'))

        json_file['woocommerce-login-nonce'] = input_list[3]
        print(json_file)
    return json_file


def get_course_links():
    with Session() as s:
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
    video_file = open("all_courses.json")
    video_json = json.load(video_file)
    video_file.close()

    with Session() as session:
        session.post("https://mescours.modestycouture.com/mon-compte/", get_credentials())

        # On crée la variable module pourse savoir ou le cours devra être placé
        module_title = ""
        for course in course_links:
            print(f"Le cours {course} est dans le module {module_title}")

            # Si le lien est un module
            if re.search("^https://mescours.modestycouture.com/module/", course):
                module_page = session.get(course).content.decode('utf-8')
                soup = BeautifulSoup(module_page, "html.parser")
                module_title = soup.select('h1')[0].text.strip()
                video_json[module_title] = {"nom du cours": ["vimeo_link"]}

            elif re.search("^https://mescours.modestycouture.com/course/", course):
                course_page = session.get(course).content.decode('utf-8')
                soup = BeautifulSoup(course_page, "html.parser")
                video_json[module_title] = video_json[module_title] | {course: []}

                i = 0
                for iframe in soup.find_all('iframe'):
                    print(iframe.get('data-src'))
                    if re.search('^https://player.vimeo.com/', iframe.get('data-src')):
                        video_json[module_title][course].append(iframe.get('data-src'))
                    i += 1

        json_objet = json.dumps(video_json)

        with open("all_courses.json", "w") as f:
            f.write(json_objet)
            f.close()

        session.close()
