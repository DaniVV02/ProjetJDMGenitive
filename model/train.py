from jdm.signature import build_signature, normalize, build_relation_signature
from model.corpus import load_corpus
import random
from model.predict import predict_relation


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

        rel_sig = build_relation_signature(sigA, sigB)


        training_examples.append({
            "relation": relation,
            "rel_sig": rel_sig,   
            "determinant": info.get("determinant"),
            "is_det": info.get("is_det", False),
            "raw": info.get("raw")
        })

    return training_examples


def train_test_split(examples, test_ratio=0.2, seed=42):
    random.seed(seed)
    examples = examples.copy()
    random.shuffle(examples)

    split = int(len(examples) * (1 - test_ratio))
    train = examples[:split]
    test = examples[split:]

    return train, test

def evaluate(test_examples, relation_index):
    correct = 0

    for ex in test_examples:
        prediction = predict_relation(
            ex["termA"],
            ex["termB"],
            relation_index,
            top_k=1
        )

        if prediction[0][0] == ex["relation"]:
            correct += 1

    return correct / len(test_examples)
