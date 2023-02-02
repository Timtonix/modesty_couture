import pyjsparser
import re
import requests
from bs4 import BeautifulSoup

with requests.Session() as session:
    vimeo = session.get(
        "https://player.vimeo.com/video/652983486?h=80b076453c&portrait=0&title=1&color=fff&byline=1&autopause=0").content.decode(
        'utf-8')

    soup = BeautifulSoup(vimeo, "html.parser")

    source_script = []
    source_link = ""
    for script in soup.find_all('script'):
        if re.search("window.playerConfig", script.text):
            # On découpe la string si elle a le tag URL
            x = re.split("url", script.text)
            for i in range(len(x)):
                # Si on a un .mp4 dans la liste
                if re.search("\.mp4", x[i]):
                    # On découpe à tous les "
                    without_comma = re.split("\"", x[i])
                    print(without_comma)
                    # Maintenant on ne récupère que le 720p
                    for iterateur in range(len(without_comma)):
                        if re.search("720p", without_comma[iterateur]):
                            print(without_comma)
                            source_link = without_comma[2]


def download_video_series(video_links: list):
    for link in video_links:

        '''iterate through all links in video_links 
        and download them one by one'''

        # obtain filename by splitting url and getting
        # last string
        file_name = "moimeme.mp4"

        print("Downloading file:%s" % file_name)

        # create response object
        r = requests.get(link, stream=True)

        # download started
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        print("%s downloaded!\n" % file_name)

    print("All videos downloaded!")
    return


print(type(source_link))
print(source_link)
download_video_series([source_link])
