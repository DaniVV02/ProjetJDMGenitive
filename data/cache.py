import os
import pickle

CACHE_DIR = "cache"
NODE_CACHE_FILE = os.path.join(CACHE_DIR, "node_cache.pkl")
SIGNATURE_CACHE_FILE = os.path.join(CACHE_DIR, "signature_cache.pkl")

# Créer le dossier cache si besoin
os.makedirs(CACHE_DIR, exist_ok=True)


def load_cache(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return {}


def save_cache(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)
        
def save_all_caches():
    save_cache(NODE_CACHE, NODE_CACHE_FILE)
    save_cache(SIGNATURE_CACHE, SIGNATURE_CACHE_FILE)


# Chargement des caches persistants
NODE_CACHE = load_cache(NODE_CACHE_FILE)
SIGNATURE_CACHE = load_cache(SIGNATURE_CACHE_FILE)
