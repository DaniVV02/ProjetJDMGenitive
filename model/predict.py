# model/predict.py
from model.similarity import cosine_similarity
from jdm.signature import build_signature, normalize

def predict_relation(termA: str, termB: str, relation_index: dict, top_k=3):
    sigA = normalize(build_signature(termA))
    sigB = normalize(build_signature(termB))

    scores = {}

    for relation, examples in relation_index.items():
        best_score = 0.0
        for ex in examples:
            scoreA = cosine_similarity(sigA, ex["sigA"])
            scoreB = cosine_similarity(sigB, ex["sigB"])
            score = (scoreA + scoreB) / 2

            if score > best_score:
                best_score = score

        scores[relation] = best_score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
