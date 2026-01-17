import os

from jdm.api import get_node_by_name
from jdm.signature import build_signature
from data.cache import save_all_caches

from model.train import build_training_set, index_by_relation
from model.predict import predict_relation


def main():
    print("Initialisation du système...\n")

    # =========================
    # 1. Test API JDM
    # =========================
    print("Test API JDM (animal):")
    print(get_node_by_name("animal"))
    print("------------------------------------")

    # =========================
    # 2. Test signature
    # =========================
    print("Signature de 'chat' (extrait):")
    sig = build_signature("chat")
    for k, v in list(sig.items())[:10]:
        print(k, v)
    print("------------------------------------")

    # =========================
    # 3. Chargement COMPLET du corpus
    # =========================
    all_examples = []

    for file in os.listdir("data/corpus_json"):
        if file.endswith(".json"):
            path = os.path.join("data/corpus_json", file)
            all_examples.extend(build_training_set(path))

    print(f"Nombre total d'exemples dans le corpus : {len(all_examples)}")
    print("------------------------------------")

    # =========================
    # 4. Entraînement FINAL du modèle
    # =========================
    relation_index = index_by_relation(all_examples)
    print("Modèle entraîné sur tout le corpus.")
    print("------------------------------------")

    # =========================
    # 5. Tests simples
    # =========================
    print("Tests de prédiction:")
    print("peinture / paysage →",
          predict_relation("peinture", "paysage", relation_index))
    print("cuillère / bois →",
          predict_relation("cuillère", "bois", relation_index))

    # =========================
    # 6. Sauvegarde du cache persistant
    # =========================
    save_all_caches()
    print("Cache sauvegardé.")


if __name__ == "__main__":
    main()
