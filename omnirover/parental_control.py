
def parental_guard(age, action):

    blocked_actions = [
        "payment",
        "crypto_purchase",
        "adult_content",
        "gambling"
    ]

    if age < 18 and action in blocked_actions:
        return {
            "allowed": False,
            "reason": "Parental restriction active"
        }

    return {
        "allowed": True
    }

