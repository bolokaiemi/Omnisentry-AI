def reputation_check(domain):

    suspicious = [
        "free-money",
        "hack-account",
        "crypto-win"
    ]

    for word in suspicious:

        if word in domain:
            return "HIGH"

    return "LOW"