def detect_payment_request(content: str):

    payment_words = [

        "credit card",
        "debit card",
        "cvv",
        "bank account",
        "wire transfer",
        "payment"

    ]

    content = content.lower()

    for word in payment_words:

        if word in content:
            return True

    return False