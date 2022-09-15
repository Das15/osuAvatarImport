import logging
import time
import requests
import apiRequests.cache as cache
import config


def request_user_id(username: str) -> str:
    api_key = config.get_config_value("bancho_api_key")

    data = {"k": api_key, "u": username, "type": "string"}
    logging.info(f"Getting user_id for username '{username}' from bancho.")

    time.sleep(0.6)

    re = requests.get("https://osu.ppy.sh/api/get_user", params=data)
    if int(re.status_code) != 200:
        raise Exception(f"Expected status code 200, got instead {re.status_code}")
    try:
        json_data = re.json()[0]
        user_id = json_data["user_id"]
    except IndexError:
        logging.error(f"Didn't found {username} on bancho.")
        user_id = None
    return user_id


def check_if_user_id_exists(userId: str):
    api_key = config.get_config_value("bancho_api_key")
    if cache.check_cache(userId):
        return True
    data = {"k": api_key, "u": userId, "type": "id"}
    logging.info(f"Checking if user with ID {userId} exists.")
    re = requests.get("https://osu.ppy.sh/api/get_user", params=data)
    if int(re.status_code) == 200 and re.json() != []:
        return True
    return False


def get_user_id(username: str):
    cache_check_result = cache.check_cache(username)
    if cache_check_result:
        return cache_check_result
    userId = request_user_id(username)
    if userId is not None:
        cache.add_entry_to_cache(username, userId)
    return userId
