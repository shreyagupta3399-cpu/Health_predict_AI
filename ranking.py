import random
import csv

def load_precautions():
    precautions_dict = {}

    with open("symptom_precaution.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            precautions = []

            for i in range(1, 5):
                precaution = row[f"Precaution_{i}"]

                if precaution.strip():
                    precautions.append(precaution)

            precautions_dict[row["Disease"]] = precautions

    return precautions_dict

def fake_model():
    probabilities = [random.random() for _ in range(41)]

    total = sum(probabilities)

    probabilities = [p / total for p in probabilities]

    return probabilities
def get_top3(probabilities, disease_names, precautions_dict, threshold=45):

    results = []

    for disease, probability in zip(disease_names, probabilities):

        confidence = probability * 100

        results.append({
            "disease": disease,
            "confidence": round(confidence, 2),
            "precautions": precautions_dict.get(
                disease,
                "Please consult a doctor."
            )
        })

    # Highest confidence first
    results.sort(
        key=lambda x: x["confidence"],
        reverse=True
    )

    # Select top 3
    top3 = results[:3]

    # Doctor warning
    if top3[0]["confidence"] < threshold:
        return {
            "results": top3,
            "consult_doctor": True,
            "warning": "Low confidence. Please consult a doctor."
        }

    return {
        "results": top3,
        "consult_doctor": False
    }
if __name__ == "__main__":
    import pickle

    precautions_dict = load_precautions()

    # Load disease names from trained model
    with open("model.pkl", "rb") as file:
        model = pickle.load(file)

    disease_names = model.classes_.tolist()

    # Test with fake probabilities
    probabilities = fake_model()

    result = get_top3(
        probabilities,
        disease_names,
        precautions_dict
    )

    print("\n===== TOP 3 TEST RESULT =====")

    for item in result["results"]:
        print(f"\nDisease: {item['disease']}")
        print(f"Confidence: {item['confidence']}%")
        print(f"Precautions: {item['precautions']}")

    if result["consult_doctor"]:
        print("\n⚠️", result["warning"])