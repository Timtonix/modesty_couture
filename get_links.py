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
    return json_file


def get_course_links():
    with Session() as s:
        s.post("https://mescours.modestycouture.com/mon-compte/", get_credentials())
        home_page = s.get("https://mescours.modestycouture.com/espace-membre/formation-modesty-couture-class/").content.decode('utf-8')
        soup = BeautifulSoup(home_page, "html.parser")
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

        print("Links have been downloaded")

# TEST comment
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


def download_video(video_directory):
    course_links = get_file_links()
    default_dir = os.listdir("./")

    if video_directory not in default_dir:
        os.mkdir(video_directory)

    with Session() as session:
        session.post("https://mescours.modestycouture.com/mon-compte/", get_credentials())

        # On crée la variable module pourse savoir ou le cours devra être placé
        for course in course_links:

            # Si le lien est un module
            if re.search("^https://mescours.modestycouture.com/module/", course):
                iterateur_cours_directory = 0
                module_page = session.get(course).content.decode('utf-8')
                soup = BeautifulSoup(module_page, "html.parser")
                module_title = soup.select('h1')[0].text.strip()

                # On vérifie si on doit créer un dossier avec le nom du module
                directory = os.listdir(f"{video_directory}/")
                if module_title not in directory:
                    try:
                        os.mkdir(f"{video_directory}/{module_title}/")
                    except OSError as e:
                        print(e)
                else:
                    print(f"Module {module_title} already exist")

            # Si c'est un cours
            elif re.search("^https://mescours.modestycouture.com/course/", course):
                # On rajoute une itération pour le dossier cours
                iterateur_cours_directory += 1
                # On va chercher la page web du cours
                course_page = session.get(course).content.decode('utf-8')
                soup = BeautifulSoup(course_page, "html.parser")
                course_title = soup.select('h1')[0].text.strip()

                course_directory_title = f"{iterateur_cours_directory} - {course_title}"
                iterateur_video = 0
                for iframe in soup.find_all('iframe'):
                    if re.search('^https://player.vimeo.com/', iframe.get('data-src')):

                        iterateur_video += 1
                        video_title = f"{iterateur_video} - {course_title}.mp4"

                        # D'abord on vérifie si le dossier n'existe pas
                        directory = os.listdir(f"{video_directory}/{module_title}/")
                        if course_directory_title not in directory:
                            try:
                                os.mkdir(f"{video_directory}/{module_title}/{course_directory_title}/")
                            except OSError as e:
                                print(e)
                        else:
                            print(f"Directory {course_directory_title} already exist")

                        # On récupère le lien source
                        source_link = get_source_link(iframe.get('data-src'))
                        file_name = f"./{video_directory}/{module_title}/{course_directory_title}/{video_title}"
                        directory = os.listdir(f"{video_directory}/{module_title}/{course_directory_title}/")

                        print(f"Vidéos in the directory are : {directory}")
                        if f"{video_title}" not in directory:

                            print("Downloading file:%s" % course_directory_title)

                            # create response object
                            r = session.get(source_link, stream=True)

                            # download started
                            with open(file_name, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=1024 * 1024):
                                    if chunk:
                                        f.write(chunk)
                            print("%s downloaded!\n" % file_name)

                        else:
                            print(f"Course {video_title} already exist")


        session.close()


def get_source_link(vimeo_link):
    with Session() as session:
        vimeo = session.get(
            vimeo_link).content.decode(
            'utf-8')

        soup = BeautifulSoup(vimeo, "html.parser")

        for script in soup.find_all('script'):
            if re.search("window.playerConfig", script.text):
                # On découpe la string si elle a le tag URL
                x = re.split("url", script.text)
                for i in range(len(x)):
                    # Si on a un .mp4 dans la liste
                    if re.search("\.mp4", x[i]):
                        # On découpe à tous les "
                        without_comma = re.split("\"", x[i])
                        # Maintenant on ne récupère que le 720p
                        for iterateur in range(len(without_comma)):
                            if re.search("720p", without_comma[iterateur]):
                                return without_comma[2]
