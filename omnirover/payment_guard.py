
def check_payment_page(page_data):

    indicators = [
        "credit card",
        "cvv",
        "bank transfer"
    ]

    found = []

    for item in indicators:
        if item in page_data.lower():
            found.append(item)

    suspicious = False

    if "unverified" in page_data.lower():
        suspicious = True

    return {
        "payment_detected": len(found) > 0,
        "fields": found,
        "suspicious": suspicious
    }

