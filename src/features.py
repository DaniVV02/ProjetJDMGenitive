from __future__ import annotations
import math
from typing import Dict, Tuple
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from .models import Prep, Article, RelationInstance

def build_encoders() -> Tuple[OneHotEncoder, OneHotEncoder]:
    def fit(values):
        enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore", dtype=np.float32)
        enc.fit(np.array(values).reshape(-1, 1))
        return enc
    return fit([p.value for p in Prep]), fit([a.value for a in Article])

def encode_syntax(rel: RelationInstance, prep_enc: OneHotEncoder, art_enc: OneHotEncoder) -> np.ndarray:
    prep_vec = prep_enc.transform([[rel.prep.value]])[0]
    if rel.determinant:
        art_vec = art_enc.transform([[rel.determinant.value]])[0]
    else:
        art_vec = np.zeros(len(art_enc.categories_[0]), dtype=np.float32)
    return np.concatenate([prep_vec, art_vec])

def weighted_jaccard(d1: Dict[int, float], d2: Dict[int, float]) -> float:
    if not d1 or not d2:
        return 0.0
    common = d1.keys() & d2.keys()
    num = sum(min(d1[n], d2[n]) for n in common)
    denom = sum(d1.values()) + sum(d2.values()) - num
    return float(num / denom) if denom > 0 else 0.0

def signed_weighted_jaccard(d1: Dict[int, float], d2: Dict[int, float], alpha: float = 0.01) -> float:
    if not d1 or not d2:
        return 0.0
    d1n = {k: math.tanh(alpha * v) for k, v in d1.items()}
    d2n = {k: math.tanh(alpha * v) for k, v in d2.items()}

    d1_pos = {k: v for k, v in d1n.items() if v > 0}
    d1_neg = {k: -v for k, v in d1n.items() if v < 0}
    d2_pos = {k: v for k, v in d2n.items() if v > 0}
    d2_neg = {k: -v for k, v in d2n.items() if v < 0}

    j_pos = weighted_jaccard(d1_pos, d2_pos)
    j_neg = weighted_jaccard(d1_neg, d2_neg)

    w_pos = sum(d1_pos.values()) + sum(d2_pos.values())
    w_neg = sum(d1_neg.values()) + sum(d2_neg.values())
    total = w_pos + w_neg
    if total == 0:
        return 0.0
    return float((j_pos * w_pos - j_neg * w_neg) / total)
