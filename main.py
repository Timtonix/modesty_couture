import get_links
import argparse
import json

parser = argparse.ArgumentParser(description="Modesty Course Installer")
parser.add_argument("--username", help="Username of Modesty Couture")
parser.add_argument("--password", help="Password of Modesty Couture")
parser.add_argument("--destination_directory", help="The destination directory like : course, video...",
                    default="video")

args = parser.parse_args()

# Write credentials
login_dict = {"username": f"{args.username}", "password": f"{args.password}", "woocommerce-login-nonce": "token",
              "_wp_http_referer": "/mon-compte/", "login": "Identification"}
login_object = json.dumps(login_dict, indent=4)
with open('login.json', "w") as file:
    file.write(login_object)

print("Writing all the links in links.txt")
get_links.get_course_links()

print("DOWNLOADING THE COURSE")
get_links.download_video(args.destination_directory)
