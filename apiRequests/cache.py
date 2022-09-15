import os

# I definitely didn't copy this from older code from lazerFiller.
CACHE_PATH = os.path.join(os.getcwd(), "cache", "bancho")


def read_cache():
    if not os.path.exists(CACHE_PATH):
        if not os.path.exists("cache"):
            os.mkdir("cache")
        return None
    with open(CACHE_PATH, "r") as file:
        temp = file.readlines()
    cache = parse_cache(temp)
    if not cache:
        return None
    return cache


def parse_cache(cache):
    temp = []
    for i in range(len(cache)):
        cache[i] = cache[i].replace("\n", "")
        if cache[i] == "":
            continue
        temp.append(cache[i].split("\t"))
    return temp


def add_entry_to_cache(username, user_id):
    with open(CACHE_PATH, "a") as file:
        file.write(f"{username}\t{user_id}\n")


def check_cache(username):
    cache = read_cache()
    if cache is None:
        return None
    for entry in cache:
        if username == entry[0]:
            return entry[1]
    return None
