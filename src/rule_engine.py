class RuleEngine:
    def __init__(self, graph):
        self.graph = graph

    def run(self):
        """Lance le moteur de règles jusqu'à stabilisation du graphe."""
        iterations = 0
        modified = True
        
        while modified:
            modified = False
            iterations += 1
            print(f"\n--- Itération du moteur de règles n°{iterations} ---")
            
            # Ici on appelle nos différentes familles de règles
            if self.rule_group_nominal(): modified = True
            # if self.rule_tagger_simple(): modified = True 
            
            # Sécurité pour éviter les boucles infinies
            if iterations > 100: 
                print("Arrêt : Trop d'itérations !")
                break
        
        print(f"Moteur terminé en {iterations} itérations.")

    def rule_group_nominal(self):
        """
        Règle simplifiée : Si NOEUD(le) --r_succ--> NOEUD(petit chat)
        Alors on peut créer un lien ou un nouveau noeud GN.
        """
        has_changed = False
        
        # On parcourt tous les arcs r_succ existants
        for edge in list(self.graph.edges): # Utiliser list() pour pouvoir modifier le graphe pendant le parcours
            if edge.type == "r_succ" and edge.weight > 0:
                n1 = edge.source
                n2 = edge.target
                
                # Exemple de condition : n1 est "le" et n2 est "petit chat"
                if n1.label == "le" and n2.label == "petit chat":
                    # On vérifie si on n'a pas déjà créé ce GN
                    if not any(e.type == "r_is_member_of" for e in self.graph.edges if e.source == n1):
                        print(f"[Règle GN] Création d'un Groupe Nominal pour '{n1.label}' + '{n2.label}'")
                        
                        gn_node = self.graph.create_node("GN:le petit chat", type="SYNTAX", weight=100)
                        self.graph.add_edge(n1, gn_node, "r_is_member_of", weight=10)
                        self.graph.add_edge(n2, gn_node, "r_is_member_of", weight=10)
                        
                        has_changed = True
        
        return has_changed
    
    def tagger_with_jdm(self, jdm_client):
        """Parcourt les mots et ajoute leurs natures JDM au graphe."""
        modified = False
        for node_id, node in list(self.graph.nodes.items()):
            if node.type in ["TERM", "TERM_COMPOUND"]:
                # Si on n'a pas encore de relation r_pos pour ce mot
                if not any(e.type == "r_pos" for e in self.graph.edges if e.source == node):
                    
                    natures = jdm_client.get_pos(node.label)
                    for nat in natures:
                        # Création du nœud POS (ex: Nom:, Verbe:)
                        pos_node = self.graph.create_node(nat, type="POS", weight=50)
                        self.graph.add_edge(node, pos_node, "r_pos", weight=10)
                        modified = True
        return modified