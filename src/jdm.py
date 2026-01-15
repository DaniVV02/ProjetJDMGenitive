from __future__ import annotations
import json, time
from pathlib import Path
from typing import Dict, List
import requests
from tqdm import tqdm
from .models import ApiCall, Node

BASE = "https://jdm-api.demo.lirmm.fr/v0"

def fetch_relations_from(term: str) -> list[dict] | None:
    url = f"{BASE}/relations/from/{term}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json().get("relations", [])

def ensure_cache_file(cache_dir: Path, rel_id: int) -> ApiCall:
    cache_dir.mkdir(parents=True, exist_ok=True)
    f = cache_dir / f"infos_by_name_{rel_id}.json"
    if f.exists():
        return ApiCall(**json.loads(f.read_text(encoding="utf-8")))
    return ApiCall(id_relation=rel_id, relation_nodes={})

def save_cache(cache_dir: Path, rel_id: int, api: ApiCall) -> None:
    f = cache_dir / f"infos_by_name_{rel_id}.json"
    f.write_text(api.model_dump_json(indent=2), encoding="utf-8")

def build_signature(term: str, rel_id: int, cache_dir: Path) -> Dict[int, float]:
    f = cache_dir / f"infos_by_name_{rel_id}.json"
    if not f.exists():
        return {}
    api = ApiCall(**json.loads(f.read_text(encoding="utf-8")))
    nodes = api.relation_nodes.get(term, [])
    return {n.node2: n.weight for n in nodes}

def fetch_vocabulary(vocab_path: Path, cache_dir: Path, rel_id: int, delay: float = 0.4):
    vocab = json.loads(vocab_path.read_text(encoding="utf-8"))
    api = ensure_cache_file(cache_dir, rel_id)

    for term in tqdm(vocab, desc=f"JDM rel={rel_id}"):
        if term in api.relation_nodes:
            continue
        try:
            rels = fetch_relations_from(term)
            filtered = [x for x in rels if x.get("type") == rel_id]
            nodes: List[Node] = [
                Node(id_node=x["id"], node1=x["node1"], node2=x["node2"], weight=float(x["w"]))
                for x in sorted(filtered, key=lambda z: z["w"], reverse=True)
            ]
            api.relation_nodes[term] = nodes
            save_cache(cache_dir, rel_id, api)
            time.sleep(delay)
        except Exception:
            # si un terme foire, on passe au suivant (à toi d’améliorer les logs)
            continue
