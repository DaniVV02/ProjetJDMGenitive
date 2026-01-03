from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List
import typer
from tqdm import tqdm
from .models import RelationInstance, RelProto, Corpus
from .jdm import build_signature
from .features import signed_weighted_jaccard

app = typer.Typer()

def load_json_corpus(fp: Path) -> List[RelationInstance]:
    data = json.loads(fp.read_text(encoding="utf-8"))
    return [RelationInstance(**v) for v in data.get("data", {}).values()]

def merged_signature(term: str, rel_ids: List[int], cache_dir: Path) -> Dict[int, float]:
    merged: Dict[int, float] = {}
    for rid in rel_ids:
        sig = build_signature(term, rid, cache_dir)
        for k, v in sig.items():
            merged[k] = merged.get(k, 0.0) + float(v)  # somme (pas overwrite)
    return merged

def absorb(proto: RelProto, a: Dict[int,float], b: Dict[int,float]) -> None:
    for d, new_d in [(proto.nodes_a, a), (proto.nodes_b, b)]:
        for k, v in new_d.items():
            d[k] = d.get(k, 0.0) + float(v)
    proto.fusion_number += 1

def update_prototypes(protos: List[RelProto], rel: RelationInstance, rel_ids: List[int], cache_dir: Path, threshold: float) -> List[RelProto]:
    a = merged_signature(rel.termA.name, rel_ids, cache_dir)
    b = merged_signature(rel.termB.name, rel_ids, cache_dir)

    for p in protos:
        score = (signed_weighted_jaccard(p.nodes_a, a) + signed_weighted_jaccard(p.nodes_b, b)) / 2
        if score >= threshold:
            absorb(p, a, b)
            return protos

    protos.append(RelProto(
        gen_type=rel.relation_type,
        termA=rel.termA.name,
        termB=rel.termB.name,
        nodes_a=a,
        nodes_b=b,
        fusion_number=0
    ))
    return protos

@app.command()
def generate_rules(corpus_dir: Path, cache_dir: Path, output_dir: Path, rel_ids: List[int] = [6,36], threshold: float = 0.30):
    output_dir.mkdir(parents=True, exist_ok=True)
    for fp in corpus_dir.glob("*.json"):
        label = fp.stem
        rels = load_json_corpus(fp)
        protos: List[RelProto] = []
        for r in tqdm(rels, desc=f"rules:{label}"):
            protos = update_prototypes(protos, r, rel_ids, cache_dir, threshold)

        out = output_dir / f"{label}_rules.json"
        out.write_text(json.dumps([p.model_dump() for p in protos], ensure_ascii=False, indent=2), encoding="utf-8")
        typer.echo(f"✔ wrote {out} ({len(protos)} protos)")
