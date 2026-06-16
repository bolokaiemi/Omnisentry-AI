def detect_fraud(content: str):

    patterns = [

        "send money",
        "wire transfer",
        "gift card",
        "crypto payment"

    ]

    found = []

    content = content.lower()

    for item in patterns:

        if item in content:
            found.append(item)

    return {

        "fraud_detected":
            len(found) > 0,

        "patterns":
            found
    }