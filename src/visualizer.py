class BratVisualizer:
    @staticmethod
    def export(graph, filename="output"):
        # 1. Générer le .txt (les mots du graphe dans l'ordre)
        # 2. Générer le .ann
        with open(f"{filename}.ann", "w", encoding="utf-8") as f:
            # Exemple de format BRAT : T1  Organization 0 10  Microsoft
            # R1  Origin Arg1:T3 Arg2:T2
            for i, node in graph.nodes.items():
                if node.type == "TERM":
                    # On écrit l'entité (très simplifié)
                    f.write(f"T{node.id}\t{node.type}\t0 0\t{node.label}\n")
            
            for i, edge in enumerate(graph.edges):
                if edge.weight > 0 and edge.type != "r_succ":
                    f.write(f"R{i}\t{edge.type} Arg1:T{edge.source.id} Arg2:T{edge.target.id}\n")
        print(f"Export BRAT terminé : {filename}.ann")