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
