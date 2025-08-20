def heart_attack_risk():
    print("Heart Disease Risk Evaluation (0 - 100 scale)\n")
    print("Please answer with 'yes' or 'no'")

    # Expanded symptoms + risk factors with weights
    factors = {
        # Major symptoms
        "Do you experience chest pain or discomfort?": 20,
        "Do you often feel shortness of breath (even at rest)?": 15,
        "Do you feel extreme fatigue or weakness often?": 10,
        "Do you have palpitations (fast or irregular heartbeat)?": 10,
        "Do you feel dizziness or lightheadedness frequently?": 10,
        "Do you experience swelling in legs, ankles, or feet?": 10,
        "Do you have nausea or cold sweats often?": 5,

        # Medical conditions / risk factors
        "Do you have high blood pressure?": 10,
        "Do you have high cholesterol?": 10,
        "Do you have diabetes?": 10,
        "Do you smoke regularly?": 10,
        "Do you drink alcohol excessively?": 5,
        "Do you have obesity or overweight issues?": 10,
        "Do you have a sedentary (inactive) lifestyle?": 5,

        # Family / age factors
        "Do you have a family history of heart disease?": 5,
        "Are you above 55 years (men) or 65 years (women)?": 5,
        "Do you have high stress levels?": 5
    }

    score = 0
    for question, weight in factors.items():
        ans = input(question + " (yes/no): ").strip().lower()
        if ans == "yes":
            score += weight

    # Cap at 100
    score = min(score, 100)

    print(f"\nEstimated likelihood of heart disease: {score}/100")
    if score < 30:
        print("Low risk – Maintain a healthy lifestyle.")
    elif score < 60:
        print("Moderate risk – Consider lifestyle changes and regular check-ups.")
    else:
        print("High risk – Please consult a doctor immediately.")

if __name__ == "__main__":
    heart_attack_risk()
