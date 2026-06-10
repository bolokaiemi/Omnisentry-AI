
# ==========================================
# OMMINSENTIRY AI
# WEBSITE ANALYZER
# ==========================================

from src.domain_checker import check_domain
from src.ssl_checker import check_ssl
from src.reputation_checker import reputation_check
from src.location_checker import get_location
from src.scoring import calculate_score

import pickle


# ==========================================
# LOAD MODEL
# ==========================================

try:

    with open(
        "models/trust_model.pkl",
        "rb"
    ) as f:

        model = pickle.load(f)

except Exception:

    model = None


# ==========================================
# WEBSITE ANALYSIS
# ==========================================

def analyze_website(domain: str):

    domain_info = check_domain(
        domain
    )

    ssl_status = check_ssl(
        domain
    )

    reputation = reputation_check(
        domain
    )

    location = get_location(
        domain
    )

    score = calculate_score(
        domain_info["age_days"],
        ssl_status,
        reputation
    )

    risk_level = "SAFE"

    if score < 70:
        risk_level = "MEDIUM"

    if score < 40:
        risk_level = "HIGH"

    if score < 20:
        risk_level = "CRITICAL"

    ai_prediction = None

    if model:

        try:

            ai_prediction = int(
                model.predict(
                    [[
                        domain_info["age_days"],
                        int(ssl_status)
                    ]]
                )[0]
            )

        except Exception:

            ai_prediction = None

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
            score,

        "risk_level":
            risk_level,

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
