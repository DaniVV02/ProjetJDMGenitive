from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import joblib
import typer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
from .features import build_encoders
from .models import RelProto, RelationInstance
from .jdm import build_signature
from .features import signed_weighted_jaccard, encode_syntax

app = typer.Typer()

def load_rules(rules_dir: Path) -> list[RelProto]:
    all_rules = []
    for fp in sorted(rules_dir.glob("*_rules.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        all_rules.extend(RelProto(**r) for r in data)
    return all_rules

def load_json_corpus(fp: Path) -> list[RelationInstance]:
    data = json.loads(fp.read_text(encoding="utf-8"))
    return [RelationInstance(**v) for v in data.get("data", {}).values()]

def sig(term: str, rel_ids: list[int], cache_dir: Path) -> dict[int,float]:
    merged = {}
    for rid in rel_ids:
        for k,v in build_signature(term, rid, cache_dir).items():
            merged[k] = merged.get(k, 0.0) + float(v)
    return merged

@app.command()
def build_features(corpus_dir: Path, rules_dir: Path, cache_dir: Path, out_dir: Path, rel_ids: list[int] = [6,36]):
    out_dir.mkdir(parents=True, exist_ok=True)
    prep_enc, art_enc = build_encoders()
    rules = load_rules(rules_dir)

    rule_ids = [f"{r.gen_type}_{i}" for i, r in enumerate(rules)]

    for fp in corpus_dir.glob("*.json"):
        label = fp.stem
        rels = load_json_corpus(fp)
        X, y = [], []
        for rel in rels:
            a = sig(rel.termA.name, rel_ids, cache_dir)
            b = sig(rel.termB.name, rel_ids, cache_dir)

            sims = []
            for rule in rules:
                simA = signed_weighted_jaccard(a, rule.nodes_a)
                simB = signed_weighted_jaccard(b, rule.nodes_b)
                sims.append((simA + simB) / 2)

            vec = np.concatenate([np.array(sims, dtype=np.float32), encode_syntax(rel, prep_enc, art_enc)])
            X.append(vec.tolist())
            y.append(label)

        out = out_dir / f"{label}_features.json"
        out.write_text(json.dumps({"X": X, "y": y, "rule_ids": rule_ids, "rel_ids": rel_ids}, ensure_ascii=False, indent=2), encoding="utf-8")
        typer.echo(f"✔ wrote {out}")

def load_features(features_dir: Path):
    X_all, y_all = [], []
    rule_ids = None
    for fp in features_dir.glob("*_features.json"):
        d = json.loads(fp.read_text(encoding="utf-8"))
        X_all.extend(d["X"]); y_all.extend(d["y"])
        if rule_ids is None:
            rule_ids = d["rule_ids"]
    return np.array(X_all), np.array(y_all), rule_ids

@app.command()
def train(features_dir: Path, model_out: Path):
    X, y, rule_ids = load_features(features_dir)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    clf = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)

    print(classification_report(yte, pred))
    print("macro-f1:", f1_score(yte, pred, average="macro"))

    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": clf, "classes": clf.classes_.tolist(), "rule_ids": rule_ids}, model_out)
    typer.echo(f"✔ saved {model_out}")
