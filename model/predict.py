# model/predict.py
from model.similarity import cosine_similarity, relation_cosine
from jdm.signature import build_signature, normalize, build_relation_signature

def predict_relation(termA: str, termB: str, relation_index: dict, top_k=3):
    sigA = normalize(build_signature(termA))
    sigB = normalize(build_signature(termB))
    rel_sig_test = build_relation_signature(sigA, sigB)


    scores = {}

    for relation, examples in relation_index.items():
        best_score = 0.0
        for ex in examples:
            score = relation_cosine(rel_sig_test, ex["rel_sig"])

            if score > best_score:
                best_score = score

        scores[relation] = best_score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
