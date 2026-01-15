from jdm.api import get_node_by_name
from jdm.signature import build_signature
from model.train import build_training_set

from model.train import index_by_relation
from model.predict import predict_relation



def main():
    # 1. Initialisation
    print("Initialisation du système...")

    # Test API JDM
    print("Test API JDM (animal):")
    print(get_node_by_name("animal"))
    print("------------------------------------")

    # Test signature
    print("Signature de 'chat':")
    sig = build_signature("chat")
    for k, v in list(sig.items())[:10]:
        print(k, v)
    print("------------------------------------")

    # Chargement du corpus
    train_depict = build_training_set("data/corpus_json/r_depict.json")
    train_matiere = build_training_set("data/corpus_json/r_objet_matiere.json")

    print(f"Exemples r_depict: {len(train_depict)}")
    print(train_depict[0]["relation"])
    print(f"Exemples r_objet>matiere: {len(train_matiere)}")
    print("------------------------------------")
    
    # Indexation
    all_train = train_depict + train_matiere
    relation_index = index_by_relation(all_train)

    # Tests de prédiction
    print("Tests de prédiction:")

    print(predict_relation("peinture", "paysage", relation_index))
    print(predict_relation("cuillère", "bois", relation_index))


    
if __name__ == "__main__":
    main()
