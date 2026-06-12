def calculate_score(age_days_or_info, ssl_status=None, reputation=None):
    score = 100
    risk_factors = []
    
    # 1. Parse inputs
    if isinstance(age_days_or_info, dict):
        domain_info = age_days_or_info
        age_days = domain_info.get("age_days", 0)
        is_registered = domain_info.get("registered", False)
    else:
        age_days = age_days_or_info or 0
        is_registered = True if age_days > 0 else False
        
    # 2. Registration Status
    if not is_registered:
        score -= 90
        risk_factors.append("Domain is not registered")
        return 10, "CRITICAL RISK", risk_factors

    # 3. Domain Age Deductions
    if age_days < 30:
        score -= 30
        risk_factors.append(f"Domain is extremely new ({age_days} days old)")
    elif age_days < 90:
        score -= 20
        risk_factors.append(f"Domain is very new ({age_days} days old)")
    elif age_days < 180:
        score -= 10
        risk_factors.append(f"Domain is young ({age_days} days old)")
    elif age_days < 365:
        score -= 5
        risk_factors.append(f"Domain is under 1 year old ({age_days} days old)")

    # 4. SSL Status
    ssl_enabled = bool(ssl_status)
    if not ssl_enabled:
        score -= 25
        risk_factors.append("SSL/HTTPS is not enabled")

    # 5. Reputation Deductions
    if isinstance(reputation, dict):
        reputation_score = reputation.get("score", 100)
        reputation_flags = reputation.get("flags", [])
        
        rep_deduction = 100 - reputation_score
        if rep_deduction > 0:
            score -= min(rep_deduction, 50)
            for flag in reputation_flags:
                risk_factors.append(flag)
    else:
        rep_level = str(reputation).upper()
        if rep_level == "HIGH":
            score -= 50
            risk_factors.append("Domain matches high-risk pattern")
        elif rep_level == "MEDIUM":
            score -= 20
            risk_factors.append("Domain matches moderate-risk pattern")

    # Ensure score is within bounds [0, 100]
    final_score = max(0, min(score, 100))
    
    # 6. Categorize risk level
    if final_score >= 85:
        risk_level = "SAFE"
    elif final_score >= 70:
        risk_level = "LOW RISK"
    elif final_score >= 40:
        risk_level = "MEDIUM RISK"
    elif final_score >= 15:
        risk_level = "HIGH RISK"
    else:
        risk_level = "CRITICAL RISK"
        
    return final_score, risk_level, risk_factors