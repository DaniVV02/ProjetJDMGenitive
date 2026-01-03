from data.regles import RULES_DATABASE

class RuleEngine:
    def __init__(self, graph):
        self.graph = graph

    def run(self):
        modified = True
        iterations = 0
        while modified and iterations < 10:
            modified = False
            iterations += 1
            print(f"\n--- Itération n°{iterations} ---")
            
            # On boucle sur chaque règle de notre base de données
            for rule in RULES_DATABASE:
                if self.apply_generic_rule(rule):
                    modified = True
        
        print(f"Moteur arrêté après {iterations} itérations.")

    def get_pos_labels(self, term_node):
        """Récupère les labels POS (ex: 'Nom:') actifs pour un noeud donné."""
        pos_nodes = self.graph.get_neighbors(term_node, "r_pos")
        # On ne garde que ceux qui ont un poids >= 0 (pas les rejetés)
        return [n.label for n in pos_nodes if n.weight >= 0]

    def apply_generic_rule(self, rule):
        """Tente d'appliquer une règle sur tout le graphe."""
        has_changed = False
        pattern = rule["pattern"]
        
        # On parcourt tous les nœuds du graphe pour trouver un point de départ
        for start_id in list(self.graph.nodes.keys()):
            current_node = self.graph.nodes[start_id]
            
            # On vérifie si ce nœud et ses successeurs matchent le pattern
            match_sequence = self.match_pattern(current_node, pattern)
            
            if match_sequence:
                # Si ça match, on exécute l'action
                if self.execute_action(rule, match_sequence):
                    has_changed = True
        
        return has_changed

    def match_pattern(self, start_node, pattern):
        """
        Vérifie si une séquence de nœuds à partir de start_node correspond au pattern.
        Retourne la liste des nœuds TERM correspondants.
        """
        sequence = []
        current = start_node
        
        for step in pattern:
            if current is None or current.weight < 0:
                return None
            
            # Est-ce que ce nœud a le POS requis ?
            node_pos_labels = self.get_pos_labels(current)
            if step["label"] in node_pos_labels:
                sequence.append(current)
                # On passe au successeur pour la prochaine étape du pattern
                successors = self.graph.get_neighbors(current, "r_succ")
                # On prend le premier successeur actif (poids >= 0)
                current = next((s for s in successors if s.weight >= 0), None)
            else:
                return None
        
        return sequence

    def execute_action(self, rule, sequence):
        """Crée les nouveaux nœuds/arcs basés sur l'action de la règle."""
        if rule["action"] == "CREATE_GN":
            labels = [n.label for n in sequence]
            gn_label = "GN:" + "_".join(labels)
            
            # Vérifier si ce GN existe déjà pour éviter boucle infinie
            if any(n.label == gn_label for n in self.graph.nodes.values()):
                return False
                
            print(f"  [Action] {rule['name']} -> Création {gn_label}")
            gn_node = self.graph.create_node(gn_label, type="SYNTAX", weight=100)
            for n in sequence:
                self.graph.add_edge(n, gn_node, "r_is_member_of", weight=10)
            return True
        
        if rule["action"] == "NEGATE_VERB_IF_PRESENT":
            # sequence[0] est le Déterminant, sequence[1] est le Nom
            noun_node = sequence[1]
            # On cherche si ce mot a aussi un POS "Verbe:"
            all_pos = self.graph.get_neighbors(noun_node, "r_pos")
            for pos_node in all_pos:
                if "Verbe:" in pos_node.label and pos_node.weight > 0:
                    print(f"  [Action] {rule['name']} -> Désambiguïsation de '{noun_node.label}': Verbe éliminé.")
                    pos_node.weight = -100
                    return True
            
        return False
    
    def tagger_with_jdm(self, jdm_client):
        modified = False
        for node in list(self.graph.nodes.values()):
            # On ne tague que les termes qui n'ont pas encore de POS
            if node.type in ["TERM", "TERM_COMPOUND"] and node.weight >= 0:
                # Vérifier si r_pos existe déjà pour éviter les doublons
                if not any(e.type == "r_pos" for e in self.graph.edges if e.source == node):
                    natures = jdm_client.get_pos(node.label)
                    print(f"DEBUG: Natures trouvées pour {node.label} : {natures}") # <--- AJOUTE ÇA
                    if natures:
                        for nat in natures:
                            # 1. Créer le noeud POS
                            pos_node = self.graph.create_node(nat, type="POS", weight=50)
                            # 2. CRÉER L'ARC r_pos (indispensable !)
                            self.graph.add_edge(node, pos_node, "r_pos", weight=10)
                            modified = True
        return modified