# jdm/api.py
import requests
from data.cache import NODE_CACHE


BASE_URL = "https://jdm-api.demo.lirmm.fr/v0"


def get_node_by_name(word: str):
    word = word.lower()

    if word in NODE_CACHE:
        return NODE_CACHE[word]

    url = f"{BASE_URL}/node_by_name/{word}"
    r = requests.get(url)
    if r.status_code != 200:
        return None

    data = r.json()
    NODE_CACHE[word] = data
    return data


def get_relations_from(node_id: int):
    url = f"{BASE_URL}/relations/from_by_id/{node_id}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

