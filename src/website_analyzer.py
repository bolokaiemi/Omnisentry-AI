from src.domain_checker import check_domain
from src.ssl_checker import check_ssl
from src.reputation_checker import reputation_check
from src.scoring import calculate_score
from src.location_checker import get_location

import pickle
import os

# ==========================================
# LOAD AI MODEL
# ==========================================

model = None

try:

    if os.path.exists("models/trust_model.pkl"):

        with open(
            "models/trust_model.pkl",
            "rb"
        ) as f:

            model = pickle.load(f)

        print("Trust model loaded.")

except Exception as e:

    print(f"Model load error: {e}")


# ==========================================
# ANALYZE WEBSITE
# ==========================================

def analyze_website(domain):

    domain_info = check_domain(domain)

    ssl_status = check_ssl(domain)

    reputation = reputation_check(domain)

    location = get_location(domain)

    trust_score = calculate_score(
        domain_info["age_days"],
        ssl_status,
        reputation
    )

    ai_prediction = None

    if model:

        try:

            ai_prediction = int(
                model.predict([
                    [
                        domain_info["age_days"],
                        int(ssl_status)
                    ]
                ])[0]
            )

        except Exception as e:

            print(f"Prediction error: {e}")

    return {

        "domain":
            domain,

        "registered":
            domain_info["registered"],

        "age_days":
            domain_info["age_days"],

        "ssl":
            ssl_status,

        "reputation":
            reputation,

        "trust_score":
            trust_score,

        "ai_prediction":
            ai_prediction,

        "ip_address":
            location["ip_address"],

        "country":
            location["country"],

        "city":
            location["city"],

        "latitude":
            location["latitude"],

        "longitude":
            location["longitude"]
    }