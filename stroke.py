def stroke_risk():
    print("Stroke Risk Evaluation (0 - 100 scale)\n")
    print("Please answer with 'yes' or 'no'")

    # Expanded symptoms + risk factors for stroke
    factors = {
        # Stroke warning signs (BE FAST model + others)
        "Do you experience sudden weakness or numbness in face, arm, or leg (especially one side)?": 25,
        "Do you have sudden difficulty speaking or understanding speech?": 20,
        "Do you have sudden vision problems (one or both eyes)?": 10,
        "Do you have sudden dizziness, loss of balance, or trouble walking?": 10,
        "Do you have sudden severe headache with no known cause?": 10,

        # Medical conditions / risk factors
        "Do you have high blood pressure?": 15,
        "Do you have diabetes?": 10,
        "Do you have high cholesterol?": 10,
        "Do you have atrial fibrillation or irregular heartbeat?": 10,
        "Do you smoke regularly?": 10,
        "Do you drink alcohol excessively?": 5,
        "Do you have obesity or overweight issues?": 10,
        "Do you have a sedentary (inactive) lifestyle?": 5,

        # Family / age / stress
        "Do you have a family history of stroke?": 5,
        "Are you above 55 years of age?": 5,
        "Do you live under high stress?": 5
    }

    score = 0
    for question, weight in factors.items():
        ans = input(question + " (yes/no): ").strip().lower()
        if ans == "yes":
            score += weight

    # Cap score at 100
    score = min(score, 100)

    print(f"\nEstimated likelihood of stroke: {score}/100")
    if score < 30:
        print("Low risk – Maintain a healthy lifestyle.")
    elif score < 60:
        print("Moderate risk – Consider lifestyle changes and regular check-ups.")
    else:
        print("High risk – Please consult a doctor immediately.")

if __name__ == "__main__":
    stroke_risk()
