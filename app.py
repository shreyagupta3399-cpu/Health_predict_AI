import tkinter as tk
from tkinter import messagebox
from main import predict_disease


def predict():
    user_input = symptoms_entry.get()

    if not user_input.strip():
        messagebox.showwarning("Warning", "Please enter your symptoms.")
        return

    selected_symptoms = [
        symptom.strip().lower()
        for symptom in user_input.split(",")
    ]

    result = predict_disease(selected_symptoms)

    output.delete("1.0", tk.END)

    for i, item in enumerate(result["results"], 1):
        output.insert(
            tk.END,
            f"{i}. Disease: {item['disease']}\n"
            f"   Confidence: {item['confidence']}%\n"
            f"   Precautions: {item['precautions']}\n\n"
        )

    if result["consult_doctor"]:
        output.insert(
            tk.END,
            "⚠️ Low confidence. Please consult a doctor."
        )


# Window
window = tk.Tk()
window.title("Health Predict AI")
window.geometry("700x600")

# Title
title = tk.Label(
    window,
    text="HEALTH PREDICT AI",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

# Instruction
instruction = tk.Label(
    window,
    text="Enter your symptoms separated by comma",
    font=("Arial", 13)
)
instruction.pack()

# Entry
symptoms_entry = tk.Entry(
    window,
    width=70,
    font=("Arial", 12)
)
symptoms_entry.pack(pady=15)

# Button
predict_button = tk.Button(
    window,
    text="Predict Disease",
    font=("Arial", 13, "bold"),
    command=predict
)
predict_button.pack(pady=10)

# Output box
output = tk.Text(
    window,
    width=75,
    height=20,
    font=("Arial", 11)
)
output.pack(pady=15)

window.mainloop()