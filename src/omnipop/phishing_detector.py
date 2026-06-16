def detect_phishing(content: str):

    patterns = [
        "password",
        "login",
        "verify account",
        "confirm account",
        "security code",
        "credit card",
        "send money",
        "otp",
        "crypto payment"
    ]

    content = content.lower()

    count = 0

    for item in patterns:
        if item in content:
            count += 1

    is_phishing = count >= 2
    # Simple scoring: 20 points per pattern matched, capped at 100
    phishing_score = min(count * 20, 100)

    return {
        "is_phishing": is_phishing,
        "phishing_score": phishing_score
    }