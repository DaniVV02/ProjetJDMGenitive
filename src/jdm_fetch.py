from __future__ import annotations
import json
import time
from pathlib import Path
import requests
from typing import Dict, List


# -------------------------
# CONFIG
# -------------------------

BASE_URL = "https://jdm-api.demo.lirmm.fr/v0"
RELATIONS_WANTED = {6, 36}   # à adapter
SLEEP = 0.4                 # respect API


# -------------------------
# API
# -------------------------

def fetch_relations(term: str) -> List[Dict]:
    url = f"{BASE_URL}/relations/from/{term}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json().get("relations", [])


# -------------------------
# PIPELINE
# -------------------------

def build_jdm_corpus(vocab_path: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    # je vais charger que 100 relations par terme pour limiter la taille
    vocabulary = json.loads(vocab_path.read_text(encoding="utf-8"))[:100]
    all_data = {}

    for term in vocabulary:
        print(f"→ {term}")
        try:
            relations = fetch_relations(term)
        except Exception as e:
            print(f"  ⚠ erreur API : {e}")
            continue

        filtered = []
        for r in relations:
            w = float(r.get("w", 0))
            rel_type = r.get("type")

            if w <= 0:
                continue

            if rel_type not in RELATIONS_WANTED:
                continue

            filtered.append({
                "id": r.get("id"),
                "type": rel_type,
                "node1": r.get("node1"),
                "node2": r.get("node2"),
                "weight": w
            })

        all_data[term] = filtered
        time.sleep(SLEEP)

    out_path = output_dir / "jdm_positive_relations.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"✔ JDM corpus écrit : {out_path}")


# -------------------------
# EXECUTION
# -------------------------

if __name__ == "__main__":
    build_jdm_corpus(
        Path("data/vocabulary.json"),
        Path("data/jdm")
    )
