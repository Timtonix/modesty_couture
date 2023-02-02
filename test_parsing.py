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
                    # Maintenant on ne récupère que le 720p
                    for iterateur in range(len(without_comma)):
                        if re.search("720p", without_comma[iterateur]):
                            print(without_comma)
                            source_link = without_comma[2]

    print(source_link)
