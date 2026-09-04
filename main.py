import json
import pickle
import numpy as np

from ranking import load_precautions, get_top3


# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)


# Load symptom order
with open("symptom_order.json", "r", encoding="utf-8") as file:
    symptom_order = json.load(file)


# Load precautions
precautions_dict = load_precautions()


def predict_disease(selected_symptoms):

    # Create input vector
    input_data = []

    for symptom in symptom_order:
        if symptom in selected_symptoms:
            input_data.append(1)
        else:
            input_data.append(0)

    input_data = np.array(input_data).reshape(1, -1)

    # Predict probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Disease names from model
    disease_names = model.classes_.tolist()

    # Get top 3 predictions
    result = get_top3(
        probabilities,
        disease_names,
        precautions_dict
    )

    return result


# Main program
if __name__ == "__main__":

    print("===================================")
    print("       HEALTH PREDICT AI")
    print("===================================")

    print("\nEnter your symptoms separated by comma.")
    print("Example: itching, skin_rash, fatigue")

    user_input = input("\nSymptoms: ")

    selected_symptoms = [
        symptom.strip().lower()
        for symptom in user_input.split(",")
    ]

    result = predict_disease(selected_symptoms)

    print("\n========== RESULT ==========")

    for item in result["results"]:
        print(
            f"\nDisease: {item['disease']}"
            f"\nConfidence: {item['confidence']}%"
            f"\nPrecautions: {item['precautions']}"
        )

    if result["consult_doctor"]:
        print("\n⚠️", result["warning"])
    else:
        print("\nPlease consult a doctor for proper diagnosis.")