# a tester

class Node:
    def __init__(self, id, label, type="TERM", weight=0):
        self.id = id
        self.label = label  # Le mot (ex: "chat")
        self.type = type    # Ex: "N", "V", "GN"
        self.weight = weight
        self.attrs = {}     # Pour stocker genre, nombre, etc.

    def __repr__(self):
        return f"[{self.label}/{self.type}]"

class Edge:
    def __init__(self, source, target, relation_type, weight=0):
        self.source = source
        self.target = target
        self.type = relation_type # Ex: "r_succ", "r_agent"
        self.weight = weight

class SemanticGraph:
    def __init__(self):
        self.nodes = {} # Dict {id: Node}
        self.edges = [] # Liste d'Edge
        self.next_id = 0

    def add_node(self, label, type="TERM", weight=0):
        n = Node(self.next_id, label, type, weight)
        self.nodes[self.next_id] = n
        self.next_id += 1
        return n

    def add_edge(self, node_src, node_tgt, rel_type, weight=0):
        e = Edge(node_src, node_tgt, rel_type, weight)
        self.edges.append(e)

    # Méthode pour obtenir les voisins, utile pour les règles
    def get_neighbors(self, node, rel_type=None):
        # ... retourne les noeuds connectés ...
        pass