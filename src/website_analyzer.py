# Copyright (c) 2026, Ebi Emmerich-Adehor. All rights reserved.

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
    with open("models/trust_model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception:
    model = None

# ==========================================
# WEBSITE ANALYSIS
# ==========================================

def analyze_website(domain: str):
    domain = domain.lower().strip()
    
    # 1. Run checkers
    domain_info = check_domain(domain)
    ssl_status = check_ssl(domain)
    reputation = reputation_check(domain)
    location = get_location(domain)

    # 2. Calculate trust score, risk level, and risk factors
    score, risk_level, risk_factors = calculate_score(
        domain_info,
        ssl_status,
        reputation
    )

    # 3. AI Prediction
    ai_prediction = None
    if model:
        try:
            # Use 5 features matching the retrained model:
            # 1. registered (0/1)
            # 2. age_days (int)
            # 3. ssl (0/1)
            # 4. reputation_score (0-100)
            # 5. trust_score (0-100)
            feature_vector = [[
                int(domain_info["registered"]),
                domain_info["age_days"],
                int(ssl_status),
                reputation["score"],
                score
            ]]
            ai_prediction = int(model.predict(feature_vector)[0])
        except Exception:
            # Fallback to older 2-feature prediction if model not retrained yet
            try:
                feature_vector = [[
                    domain_info["age_days"],
                    int(ssl_status)
                ]]
                ai_prediction = int(model.predict(feature_vector)[0])
            except Exception:
                ai_prediction = None

    return {
        "domain": domain,
        "registered": domain_info["registered"],
        "age_days": domain_info["age_days"],
        "ssl": ssl_status,
        "reputation": reputation,
        "trust_score": score,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "ai_prediction": ai_prediction,
        "ip_address": location["ip_address"],
        "country": location["country"],
        "city": location["city"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "isp": location.get("isp", "Unknown"),
        "asn": location.get("asn", "Unknown"),
        "registrar": domain_info.get("registrar"),
        "creation_date": domain_info.get("creation_date"),
        "expiration_date": domain_info.get("expiration_date"),
        "updated_date": domain_info.get("updated_date"),
        "name_servers": domain_info.get("name_servers", []),
        "status": domain_info.get("status")
    }
