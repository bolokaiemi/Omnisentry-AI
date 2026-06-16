def analyze_behavior(content: str):

    keywords = [

        "act now",
        "urgent",
        "limited time",
        "verify immediately",
        "account suspended"

    ]

    content = content.lower()

    found = []

    for word in keywords:

        if word in content:
            found.append(word)

    return {

        "urgency":
            len(found) > 0,

        "matches":
            found
    }