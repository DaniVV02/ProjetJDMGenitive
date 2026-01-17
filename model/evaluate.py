from model.predict import predict_relation

def evaluate(test_examples, relation_index):
    correct = 0
    total = len(test_examples)

    for ex in test_examples:
        termA = ex["raw"].split()[0].lower()  # ou stocke termA directement
        termB = ex["raw"].split()[-1].lower()

        true_relation = ex["relation"]

        prediction = predict_relation(termA, termB, relation_index, top_k=1)
        predicted_relation = prediction[0][0]

        if predicted_relation == true_relation:
            correct += 1

    accuracy = correct / total if total > 0 else 0
    return accuracy
