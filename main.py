import logging
import shutil
import json
import re
from importlib import reload
from PIL import Image
import os
from os import listdir
from os.path import isfile, join
import requests
import codecs
import csv
import apiRequests.querries as querries
import time

_CACHEPATH = os.path.join(os.getcwd(), "cache")
reload(logging)
logging.basicConfig(filename="logs.log", filemode="w",
                    encoding="utf-8", format='%(asctime)s %(levelname)s - %(message)s', datefmt="%d-%m-%y %H:%M:%S")


def main():
    starting_time = time.time()
    print("Starting the script...")
    avatars_path = os.path.join(os.getcwd(), "avatars")

    get_avatars(avatars_path)
    change_extensions_to_png(avatars_path)
    print(f"Finished in {round((time.time() - starting_time) * 100) / 100} seconds.")


def get_avatars(avatars_path: str):
    usernames = get_usernames()

    if not os.path.isdir(avatars_path):
        os.mkdir(avatars_path)
    files = get_files_from_directory(avatars_path)
    if files:
        for file in files:
            os.remove(os.path.join(avatars_path, file))
    for username in usernames:
        user_id = username if username.isdigit() else querries.get_user_id(username)
        filename = parse_filename(username)
        response = get_user_image(filename, user_id)
        if response == 429:
            logging.critical("Program sent too many requests, somehow.")
            raise Exception("Too many requests.")


def get_usernames() -> []:
    usernames = []
    if os.path.isfile("bracket.json"):
        logging.info("Getting usernames from bracket.")
        get_usernames_from_bracket(usernames)
    else:
        logging.info("Loading usernames from usernames.csv")
        if not os.path.exists("usernames.csv"):
            logging.critical("Couldn't find 'usernames.csv'.")
            print("Cannot find usernames.csv.")
            exit(1)
        with open("usernames.csv", "r", encoding="utf-8") as file:
            csv_file = csv.reader(file)
            for line in csv_file:
                for entry in line:
                    usernames.append(entry)
    return usernames


def get_usernames_from_bracket(usernames: []):
    with codecs.open("bracket.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)

        for i in range(len(json_data["Teams"])):
            username = json_data["Teams"][i]["FullName"]
            json_data["Teams"][i]["FlagName"] = remove_non_ascii_chars(username)
            usernames.append(username)
    if not os.path.isfile("bracket_backup.json"):
        shutil.copy("bracket.json", "bracket_backup.json")
    with codecs.open("bracket.json", "w", encoding="utf-8") as file:
        dump = json.dumps(json_data, indent=4)
        file.write(dump)


def get_files_from_directory(path: str) -> []:
    files = [item for item in listdir(path) if isfile(join(path, item))]
    return files


def parse_filename(filename: str) -> str:
    path_regex = re.compile("[^\\w|^-|^()]")
    non_ascii_name = remove_non_ascii_chars(filename)
    return path_regex.sub("_", non_ascii_name.lower())


def change_extensions_to_png(avatars_path: str):
    files = get_files_from_directory(avatars_path)
    for file in files:
        extension = file.split(".")[-1]
        if extension in {"jpeg", "gif", "jpg"}:
            convert_to_png(file)
            logging.info("Deleting '{}'".format(file))
            os.remove(os.path.join(avatars_path, file))


def remove_non_ascii_chars(string: str) -> str:
    return "".join(char for char in string if 0 < ord(char) < 127)


def convert_to_png(image_name: str):
    filename = image_name.split(".")[0] + ".png"
    image_path = "avatars/" + image_name
    img = Image.open(image_path)
    img.save(os.path.join("avatars", filename))
    logging.info(f"Converted '{filename}' to png.")


def get_user_image(filename: str, user_id: str):
    request = requests.get("https://a.ppy.sh/{}".format(user_id))

    if request.status_code != 200:
        logging.error(f"Skipping '{user_id}', status code: '{request.status_code}'")
        return request.status_code
    image_ext = request.headers["Content-Type"].split("/")[-1]
    with open(os.path.join("avatars", filename + "." + image_ext), "wb") as f:
        f.write(request.content)


if __name__ == "__main__":
    main()
