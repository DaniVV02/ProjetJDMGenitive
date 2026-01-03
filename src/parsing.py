from __future__ import annotations
import json, re
from pathlib import Path
from typing import Dict, Any
import typer
from .models import RelationInstance, TermInfo, Prep, Article, Corpus

app = typer.Typer()

ARTICLES = {"le","la","les","l'","un","une"}
PREP_TOKENS = {p.value: p for p in Prep}

def tokenize(s: str) -> list[str]:
    # garde l' comme token
    return re.findall(r"\b\w+'\b|\b\w+\b", s)

def parse_line(line: str) -> Dict[str, Any] | None:
    line = line.strip()
    if not line or "|" not in line:
        return None

    left, label = line.split("|", 1)
    label = label.strip()
    toks = tokenize(left)

    if not toks:
        return None

    termA = toks[0].lower()

    # chercher la prep depuis la fin
    prep = None
    prep_idx = None
    for i in range(len(toks)-1, -1, -1):
        t = toks[i].upper()
        if t in PREP_TOKENS:
            prep = PREP_TOKENS[t]
            prep_idx = i
            break
        # cas "D" + "'" séparé n'arrive pas avec tokenize ici, mais on reste safe
        if t == "D" and i+1 < len(toks) and toks[i+1] == "'":
            prep = Prep.D
            prep_idx = i
            break

    if prep is None or prep_idx is None or prep_idx + 1 >= len(toks):
        return None

    det = None
    is_det = False
    termB = toks[prep_idx + 1]

    if termB.lower() in ARTICLES:
        is_det = True
        det = Article(termB.upper().replace("L'", "L'")) if termB.lower() != "l'" else Article.L
        if prep_idx + 2 >= len(toks):
            return None
        termB = toks[prep_idx + 2]

    return {
        "termA": termA,
        "termB": termB.lower(),
        "prep": prep,
        "relation_type": label,
        "is_det": is_det,
        "determinant": det,
        "raw": left.strip(),
    }

@app.command()
def parse_txt_dir(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    vocab = set()

    for txt in input_dir.glob("*.txt"):
        corpus_dict: Dict[str, RelationInstance] = {}
        with open(txt, "r", encoding="utf-8") as f:
            for line in f:
                parsed = parse_line(line)
                if not parsed:
                    continue
                rel = RelationInstance(
                    termA=TermInfo(name=parsed["termA"]),
                    termB=TermInfo(name=parsed["termB"]),
                    prep=parsed["prep"],
                    relation_type=parsed["relation_type"],
                    is_det=parsed["is_det"],
                    determinant=parsed["determinant"],
                )
                corpus_dict[parsed["raw"]] = rel
                vocab.update([rel.termA.name, rel.termB.name])

        out = output_dir / f"{txt.stem}.json"
        corpus = Corpus(original_file=txt, data=corpus_dict)
        out.write_text(corpus.model_dump_json(indent=2), encoding="utf-8")
        typer.echo(f"✔ wrote {out}")

    vocab_path = output_dir.parent / "vocabulary.json"
    vocab_path.write_text(json.dumps(sorted(vocab), ensure_ascii=False, indent=2), encoding="utf-8")
    typer.echo(f"✔ wrote {vocab_path}")
