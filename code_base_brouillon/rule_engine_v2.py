class RuleEngine:
    def __init__(self, graph, jdm_client):
        self.graph = graph
        self.jdm = jdm_client

    def apply_rules(self):
        graph_modified = True
        while graph_modified:
            graph_modified = False
            # Exemple de logique de règle : Identification des GN
            # Règle : Si DET + NOUN reliés par r_succ, alors créer GN
            for edge in self.graph.edges:
                if edge.type == "r_succ":
                    n1 = self.graph.nodes[edge.source]
                    n2 = self.graph.nodes[edge.target]
                    
                    # Vérification hypothétique
                    if n1.type == "DET" and n2.type == "NOUN":
                         # Vérifier si le GN existe déjà pour ne pas boucler
                         if not self.relation_exists(n1, n2, "part_of_GN"):
                             # ACTION : Créer le noeud GN
                             # ACTION : Lier n1 et n2 au GN
                             graph_modified = True

                             # src/rule_engine.py