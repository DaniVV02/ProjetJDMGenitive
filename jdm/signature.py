from collections import defaultdict
from jdm.api import get_node_by_name, get_relations_from

# relations JDM importantes
TYPE_RELATIONS = {6, 36}   # marqueurs de type
ISA_RELATION = 0           # r_isa

import math

def normalize(signature: dict):
    norm = math.sqrt(sum(v * v for v in signature.values()))
    if norm == 0:
        return signature
    return {k: v / norm for k, v in signature.items()}


def build_signature(word: str):
    signature = defaultdict(float)

    node = get_node_by_name(word.lower())
    if not node:
        return signature

    node_id = node["id"]
    relations_data = get_relations_from(node_id)
    if not relations_data:
        return signature

    nodes = {n["id"]: n["name"] for n in relations_data["nodes"]}

    for rel in relations_data["relations"]:
        rel_type = rel["type"]
        weight = rel["w"]
        target_id = rel["node2"]

        if rel_type in TYPE_RELATIONS or rel_type == ISA_RELATION:
            target_name = nodes.get(target_id)
            if target_name:
                signature[target_name] += max(weight, 0)

    return dict(signature)


#{
#   "_INFO-SEM-ANIMAL": 500,
#   "organisme_vivant": 125,
#   "être_vivant": 80
#}

