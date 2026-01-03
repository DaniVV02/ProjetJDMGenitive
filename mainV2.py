from src.graph import SemanticGraph
from src.preprocessor import CompoundDict 
from src.jdm_client import JDMClient
from src.rule_enginev2 import RuleEngine

def main():
    print("=== INITIALISATION DU SYSTÈME ANALYSEUR ===")
    
    # 1. Préparation des ressources
    dictionary = CompoundDict()
    # On ajoute quelques composés pour le test
    dictionary.add_compound("petit chat")
    dictionary.add_compound("lait de chèvre")
    
    jdm = JDMClient() # Gère le cache automatiquement
    graph = SemanticGraph()
    engine = RuleEngine(graph)

    # 2. Entrée du texte
    phrase = "le petit chat boit du lait de chèvre"
    print(f"\nTexte source : '{phrase}'")

    # 3. Phase 1 : Construction du squelette (Mots simples + Composés)
    graph.init_from_text_with_compounds(phrase, dictionary)

    # 4. Phase 2 : Enrichissement JDM (POS Tagging)
    # On demande à JDM de nous donner les natures de TOUS les nœuds TERM
    print("\n--- Phase d'enrichissement lexicale (JDM) ---")
    engine.tagger_with_jdm(jdm)

    # 5. Phase 3 : Application des règles (Grammaire + Désambiguïsation)
    print("\n--- Phase d'analyse sémantique (Moteur de règles) ---")
    engine.run()

    # 6. Affichage du résultat final
    print("\n=== RÉSULTAT DE L'ANALYSE (GRAPHE FINAL) ===")
    print(graph)

    # 7. Bonus : Extraction simple des relations sémantiques trouvées
    print("\n--- Relations extraites ---")
    for node in graph.nodes.values():
        if node.type == "SYNTAX": # Nos GN
            print(f"Structure trouvée : {node.label}")
        if node.type == "POS" and node.weight < 0:
            # On cherche le mot parent pour l'affichage
            for edge in graph.edges:
                if edge.target == node:
                    print(f"Ambiguïté résolue : '{edge.source.label}' n'est PAS {node.label}")

if __name__ == "__main__":
    main()