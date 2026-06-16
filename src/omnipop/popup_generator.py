def generate_popup(risk_score):

    if risk_score >= 80:

        return {
            "title":
                "HIGH RISK",

            "message":
                "Do not enter financial information."
        }

    if risk_score >= 50:

        return {
            "title":
                "WARNING",

            "message":
                "Verify this website before continuing."
        }

    return {
        "title":
            "SAFE",

        "message":
            "No immediate threats detected."
    }