from jdm.signature import build_signature, normalize
from model.corpus import load_corpus

from collections import defaultdict

def index_by_relation(training_examples):
    index = defaultdict(list)
    for ex in training_examples:
        index[ex["relation"]].append(ex)
    return index


def build_training_set(json_path: str):
    corpus = load_corpus(json_path)
    training_examples = []

    for _, info in corpus.items():
        termA = info["termA"].lower()
        termB = info["termB"].lower()
        relation = info["relation_type"]

        sigA = normalize(build_signature(termA))
        sigB = normalize(build_signature(termB))

        training_examples.append({
            "relation": relation,
            "sigA": sigA,
            "sigB": sigB,
            # on garde ces infos pour plus tard
            "determinant": info.get("determinant"),
            "is_det": info.get("is_det", False),
            "raw": info.get("raw")
        })

    return training_examples