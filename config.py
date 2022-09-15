# I definitely didn't copy this from lazerFiller.
import logging
import os


CONFIG = {}


def create_config_file(config_dictionary: {}):
    with open("config.cfg", "w", encoding="utf-8") as file:
        file.write("# API key is only used when you input usernames instead of user ids.\n")
        for key, value in config_dictionary.items():
            file.write(f"{key} = {value}\n")


def get_config_value(key: str) -> str:
    if CONFIG:
        return CONFIG[key]
    else:
        read_config()
        if CONFIG:
            return CONFIG[key]
    create_config()
    get_config_value(key)


def create_config():
    temp_config = {"bancho_api_key": input("Please paste your bancho API key here: ")}
    create_config_file(temp_config)


def read_config() -> {}:
    if not os.path.exists("config.cfg"):
        create_config()
    with open("config.cfg", "r", encoding="utf-8") as file:
        for line_count, line in enumerate(file):
            if line[0] == "#":
                continue
            temp = line.replace(" ", "").replace("\n", "")
            key, value = temp.split("=")
            CONFIG[key] = value
        logging.debug(f"Read {line_count} lines of config.")
    return CONFIG
