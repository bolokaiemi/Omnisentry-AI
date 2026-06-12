def reputation_check(domain):

    suspicious = [
        "free-money",
        "hack-account",
        "crypto-win"
    ]

    for word in suspicious:

        if word in domain:
            return {"level": "HIGH", "score": 10, "flags": ["Matches suspicious URL pattern"]}

    return {"level": "LOW", "score": 100, "flags": []}