import json

def load_corpus(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    return content["data"]
