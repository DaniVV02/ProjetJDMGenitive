import math

def cosine_similarity(vec1: dict, vec2: dict):
    if not vec1 or not vec2:
        return 0.0

    common_keys = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[k] * vec2[k] for k in common_keys)

    norm1 = math.sqrt(sum(v * v for v in vec1.values()))
    norm2 = math.sqrt(sum(v * v for v in vec2.values()))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return numerator / (norm1 * norm2)

def relation_cosine(rel1: dict, rel2: dict):
    common = set(rel1.keys()) & set(rel2.keys())
    num = sum(rel1[k] * rel2[k] for k in common)

    norm1 = sum(v*v for v in rel1.values()) ** 0.5
    norm2 = sum(v*v for v in rel2.values()) ** 0.5

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return num / (norm1 * norm2)
