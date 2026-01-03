# src/preprocessor.py
import os

class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionnaire {mot: TrieNode}
        self.is_end = False # Vrai si ce noeud marque la fin d'une expression complète
        self.label = None   # Pour stocker le mot complet (ex: "pomme de terre")

class CompoundDict:
    def __init__(self):
        self.root = TrieNode()

    def add_compound(self, expression):
        """Ajoute une expression (str) dans l'arbre."""
        # On découpe l'expression en mots : "pomme de terre" -> ["pomme", "de", "terre"]
        words = expression.split() 
        current = self.root
        for word in words:
            if word not in current.children:
                current.children[word] = TrieNode()
            current = current.children[word]
        current.is_end = True
        current.label = expression

    def load_from_file(self, filepath):
        """Charge les mots composés depuis le fichier fourni par JDM."""
        if not os.path.exists(filepath):
            print(f"Attention: Fichier {filepath} introuvable.")
            return

        print(f"Chargement des mots composés depuis {filepath}...")
        count = 0
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                # Nettoyage selon les consignes (si besoin)
                # JDM donne parfois des trucs comme "pomme de terre > légume" ou avec des pipes
                # Ici on prend la partie gauche brute pour l'exemple
                term = line.split(';')[0] # Supposons format CSV ou simple ligne
                
                self.add_compound(term)
                count += 1
        print(f"{count} termes composés chargés.")

    def find_longest_match(self, words, start_index):
        """
        Cherche la plus longue expression composée commençant à start_index.
        Retourne (l'expression trouvée, la longueur en mots) ou (None, 0).
        """
        current = self.root
        last_match = None
        match_length = 0
        
        # On parcourt les mots de la phrase à partir de start_index
        for i in range(start_index, len(words)):
            word = words[i]
            if word in current.children:
                current = current.children[word]
                if current.is_end:
                    last_match = current.label
                    match_length = (i - start_index) + 1
            else:
                break # On ne peut plus avancer dans l'arbre
        
        return last_match, match_length