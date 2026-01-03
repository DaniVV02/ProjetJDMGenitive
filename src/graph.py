# src/graph.py

class Node:
    def __init__(self, uid, label, type="TERM", weight=0):
        self.id = uid            # Identifiant unique (ex: 0, 1, 2...)
        self.label = label       # Le mot ou concept (ex: "chat", "GN")
        self.type = type         # Le type (ex: "TERM", "POS", "CONCEPT")
        self.weight = weight     # Poids (ex: 100 pour sûr, -1 pour rejeté)
        self.metadata = {}       # Fourre-tout pour : genre, nombre, lemme...

    def __repr__(self):
        # Affichage pour le débogage : [id:label/type (poids)]
        return f"[{self.id}:{self.label}/{self.type} ({self.weight})]"

class Edge:
    def __init__(self, source, target, type, weight=0):
        self.source = source     # Instance de Node
        self.target = target     # Instance de Node
        self.type = type         # Ex: "r_succ", "r_agent", "r_pos"
        self.weight = weight     # Poids de la relation

    def __repr__(self):
        return f"{self.source.id} --{self.type}--> {self.target.id}"

class SemanticGraph:
    def __init__(self):
        self.nodes = {}  # Dictionnaire {id: Node} pour accès rapide
        self.edges = []  # Liste simple des arcs
        self._next_id = 0 # Compteur interne pour les IDs

    def create_node(self, label, type="TERM", weight=0):
        """Crée un nœud, l'ajoute au graphe et le retourne."""
        new_node = Node(self._next_id, label, type, weight)
        self.nodes[self._next_id] = new_node
        self._next_id += 1
        return new_node

    def add_edge(self, source_node, target_node, type, weight=0):
        """Crée un lien orienté entre deux nœuds."""
        new_edge = Edge(source_node, target_node, type, weight)
        self.edges.append(new_edge)
        return new_edge

    def get_neighbors(self, node, relation_type=None):
        """Récupère les nœuds sortants depuis 'node', filtrés optionnellement par type."""
        result = []
        for edge in self.edges:
            # On vérifie la source ET si le poids n'est pas négatif (optionnel)
            if edge.source == node:
                if relation_type is None or edge.type == relation_type:
                    result.append(edge.target)
        return result

    def init_from_text(self, text):
        """
        Transforme une phrase brute en chaîne linéaire de nœuds reliés par r_succ.
        Ex: [_START] -> [le] -> [chat] -> [_END]
        """
        words = text.split() # Tokenisation basique (à améliorer plus tard)
        
        previous_node = self.create_node("_START", type="META")
        
        for word in words:
            current_node = self.create_node(word, type="TERM")
            # Création du lien r_succ
            self.add_edge(previous_node, current_node, "r_succ", weight=10)
            previous_node = current_node
            
        end_node = self.create_node("_END", type="META")
        self.add_edge(previous_node, end_node, "r_succ", weight=10)

    def __str__(self):
        """Affiche un résumé textuel du graphe."""
        res = "--- NOEUDS ---\n"
        for n in self.nodes.values():
            res += f"{n}\n"
        res += "--- ARCS ---\n"
        for e in self.edges:
            res += f"{e}\n"
        return res
    
    # Dans src/graph.py, ajoutez/modifiez ceci :

    def init_from_text_with_compounds(self, text, compound_dict):
        """
        Construit le graphe linéaire ET ajoute les termes composés en parallèle.
        """
        words = text.split() # Tokenisation simple (à améliorer pour la ponctuation)
        
        # 1. Construction de la chaîne linéaire de base
        # On garde une liste des nœuds créés pour pouvoir s'y référer
        nodes_list = [] 
        
        start_node = self.create_node("_START", type="META")
        nodes_list.append(start_node)
        
        previous_node = start_node
        for word in words:
            current_node = self.create_node(word, type="TERM")
            self.add_edge(previous_node, current_node, "r_succ", weight=10)
            nodes_list.append(current_node) # On stocke le noeud
            previous_node = current_node
            
        end_node = self.create_node("_END", type="META")
        self.add_edge(previous_node, end_node, "r_succ", weight=10)
        nodes_list.append(end_node)

        # 2. Détection et ajout des termes composés (Chemins parallèles)
        # nodes_list contient : [_START, mot1, mot2, mot3, ..., _END]
        # L'index 1 correspond au premier mot "réel".
        
        i = 0
        while i < len(words):
            # On cherche un composé commençant au mot 'i'
            # Note: words[i] correspond au noeud nodes_list[i+1] (car index 0 est _START)
            compound, length = compound_dict.find_longest_match(words, i)
            
            if compound:
                print(f"--> Terme composé détecté : '{compound}' (longueur {length})")
                
                # Créer le nœud unique pour le terme composé
                compound_node = self.create_node(compound, type="TERM_COMPOUND")
                
                # Trouver le point de départ et d'arrivée dans le graphe existant
                # Départ : Le noeud AVANT le début du composé
                # Si le mot commence à l'index i, le noeud précédent est à l'index i (dans nodes_list)
                source_node = nodes_list[i] 
                
                # Arrivée : Le noeud qui représente le dernier mot du composé
                # Si longueur est 3, on saute 3 mots.
                target_node = nodes_list[i + length + 1] # +1 car on veut se connecter au mot SUIVANT le composé?
                
                # ATTENTION à la logique de la consigne :
                # [du] -> [lait] -> [de] -> [chèvre] -> [_END]
                # [du] -> [lait de chèvre] -> [_END]
                # Le noeud composé est connecté depuis "du" et va vers "_END"
                
                # Connexion start -> composé
                self.add_edge(source_node, compound_node, "r_succ", weight=10)
                
                # Connexion composé -> suite (le noeud qui suit le dernier mot du composé)
                # nodes_list[i + length + 1] est le noeud juste après la séquence
                self.add_edge(compound_node, nodes_list[i + length + 1], "r_succ", weight=10)
                
                # Ici, on n'avance PAS 'i' de 'length', car on veut peut-être détecter 
                # des composés imbriqués ou qui se chevauchent (selon la complexité voulue).
                # Pour faire simple : on avance juste de 1 pour continuer à scanner.
            
            i += 1
    
