# main.py
from src.graph import SemanticGraph
from src.preprocessor import CompoundDict 
from src.jdm_client import JDMClient
from src.rule_engine import RuleEngine


def main():
    # 1. Initialisation
    print("Initialisation du système...")
    
    # Chargement du dictionnaire
    dictionary = CompoundDict()
    # Pour le test, on ajoute manuellement, mais tu décommenteras la ligne load_from_file
    # dictionary.load_from_file("data/mots_composes.txt") 
    dictionary.add_compound("pomme de terre")
    dictionary.add_compound("lait de chèvre")
    dictionary.add_compound("petit chat")

    # Création de l'instance du graphe
    jdm = JDMClient()
    graph = SemanticGraph()
    engine = RuleEngine(graph)

    # 2. Phrase d'entrée
    phrase = "le petit chat boit du lait de chèvre"
    print(f"\nTraitement de la phrase : '{phrase}'")

    # 3. Initialisation de la chaîne linéaire (r_succ)
    # graph.init_from_text(phrase)

    # 3. Construction du graphe avec les chemins parallèles pour les composés  
    graph.init_from_text_with_compounds(phrase, dictionary)

    # 4. Vérification des chemins parallèles (Exemple sur "du")
    print("\n--- Vérification des chemins parallèles ---")
    node_du = next((n for n in graph.nodes.values() if n.label == "du"), None)
    if node_du:
        print(f"Successeurs de '{node_du.label}':")
        neighbors = graph.get_neighbors(node_du, "r_succ")
        for n in neighbors:
            print(f" -> {n.label} ({n.type})") 
            # Ici tu verras bien "lait" ET "lait de chèvre"


    # 5. Simulation de l'ajout d'infos morphosyntaxiques (POS)
    print("\n--- Simulation : Ajout de natures (POS) ---")
    node_chat = next((n for n in graph.nodes.values() if n.label == "chat"), None)
    
    if node_chat:
        # On ajoute les hypothèses de JDM
        node_nom = graph.create_node("Nom:", type="POS", weight=50)
        node_verbe = graph.create_node("Verbe:", type="POS", weight=20)
        
        graph.add_edge(node_chat, node_nom, "r_pos", weight=10)
        graph.add_edge(node_chat, node_verbe, "r_pos", weight=5)
        
        print(f"Ajout de POS pour '{node_chat.label}': Nom (50) et Verbe (20)")

        # Désambiguïsation (simulation d'une règle)
        print("[Règle] Désambiguïsation : Dans ce contexte, 'chat' n'est pas un verbe.")
        node_verbe.weight = -100 

    # 6. Affichage final
    print("\n=== ÉTAT FINAL DU GRAPHE ===")
    print(graph)

    # 3. Lancer le moteur (qui va appeler JDM et appliquer les règles)
    print("\n--- 2e Démarrage de l'analyse ---")
    
    # Étape A : On demande à JDM les natures des mots
    engine.tagger_with_jdm(jdm)
    
    # Étape B : On lance les règles grammaticales (GN, GV, etc.)
    engine.run()

    print("\n=== ÉTAT FINAL DU GRAPHE ===")
    print(graph)
 
if __name__ == "__main__":
    main()