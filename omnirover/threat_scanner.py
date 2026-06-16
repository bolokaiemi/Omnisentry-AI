
def scan_page(page_data):

    text = page_data.lower()

    suspicious_keywords = [
        "urgent payment",
        "verify account",
        "send money now",
        "crypto payment",
        "gift card"
    ]

    detected = []

    score = 0

    for keyword in suspicious_keywords:
        if keyword in text:
            detected.append(keyword)
            score += 20

    return {
        "detected": detected,
        "risk_score": min(score, 100)
    }

