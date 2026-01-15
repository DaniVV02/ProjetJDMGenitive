from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Dict, Any


# -------------------------
# CONFIG
# -------------------------

ARTICLES = {"le", "la", "les", "l'", "un", "une"}
PREPOSITIONS = {"de", "du", "des", "d'"}


# -------------------------
# OUTILS
# -------------------------

def tokenize(text: str) -> list[str]:
    """
    Tokenisation simple, conserve d'
    """
    return re.findall(r"\b\w+'\b|\b\w+\b", text.lower())


def parse_line(line: str, label: str) -> Dict[str, Any] | None:
    """
    Parse une ligne du type :
    Peinture de paysage | r_depict
    """
    if "|" not in line:
        return None

    left, _ = line.split("|", 1)
    tokens = tokenize(left)

    if len(tokens) < 3:
        return None

    # Recherche de la préposition depuis la fin
    prep_idx = None
    prep = None
    for i in range(len(tokens) - 1, -1, -1):
        if tokens[i] in PREPOSITIONS:
            prep_idx = i
            prep = tokens[i]
            break

    if prep_idx is None or prep_idx + 1 >= len(tokens):
        return None

    termA = tokens[0]
    termB = tokens[prep_idx + 1]

    is_det = False
    determinant = None

    if termB in ARTICLES:
        is_det = True
        determinant = termB
        if prep_idx + 2 >= len(tokens):
            return None
        termB = tokens[prep_idx + 2]

    return {
        "termA": termA,
        "termB": termB,
        "preposition": prep,
        "determinant": determinant,
        "is_det": is_det,
        "relation_type": label,
        "raw": left.strip()
    }


# -------------------------
# PIPELINE PRINCIPAL
# -------------------------

def parse_txt_dir(txt_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    vocabulary = set()

    for txt_file in txt_dir.glob("*.txt"):
        label = txt_file.stem
        corpus = {}

        with open(txt_file, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                parsed = parse_line(line.strip(), label)
                if not parsed:
                    continue

                corpus[f"{label}_{i}"] = parsed
                vocabulary.add(parsed["termA"])
                vocabulary.add(parsed["termB"])

        out_path = output_dir / f"{label}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "label": label,
                    "data": corpus
                },
                f,
                indent=2,
                ensure_ascii=False
            )

        print(f"✔ écrit : {out_path}")

    vocab_path = output_dir.parent / "vocabulary.json"
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(sorted(vocabulary), f, indent=2, ensure_ascii=False)

    print(f"✔ vocabulaire : {vocab_path}")


# -------------------------
# EXECUTION
# -------------------------

if __name__ == "__main__":
    parse_txt_dir(
        Path("data/txt"),
        Path("data/corpus_json")
    )
