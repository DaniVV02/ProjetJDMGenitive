# jdm/api.py
import requests

BASE_URL = "https://jdm-api.demo.lirmm.fr/v0"

def get_node_by_name(word: str):
    url = f"{BASE_URL}/node_by_name/{word}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def get_relations_from(node_id: int):
    url = f"{BASE_URL}/relations/from_by_id/{node_id}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
