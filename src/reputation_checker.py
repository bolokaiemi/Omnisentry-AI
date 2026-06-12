def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def get_base_domain_parts(domain):
    domain = domain.lower().strip()
    parts = domain.split('.')
    if len(parts) < 2:
        return domain, "", ""
    
    # Check for double extensions like .co.uk
    if len(parts) >= 3 and parts[-2] in ("co", "com", "net", "org", "edu", "gov", "mil", "ac") and len(parts[-1]) == 2:
        sld = parts[-3]
        tld = ".".join(parts[-2:])
        base_domain = ".".join(parts[-3:])
    else:
        sld = parts[-2]
        tld = parts[-1]
        base_domain = ".".join(parts[-2:])
        
    return base_domain, sld, tld

def reputation_check(domain):
    domain = domain.lower().strip()
    base_domain, sld, tld = get_base_domain_parts(domain)
    
    score = 100
    flags = []
    
    # 1. Suspicious Keywords Check
    suspicious_keywords = [
        "free-money", "hack-account", "crypto-win", "login", "signin",
        "secure", "verify", "verification", "account", "update",
        "banking", "giveaway", "claim", "prize", "bonus", "billing",
        "support", "admin", "wallet", "metamask", "trustwallet",
        "coinbase", "binance", "gift", "refund", "card", "payment"
    ]
    
    matched_keywords = []
    for word in suspicious_keywords:
        if word in sld:
            matched_keywords.append(word)
            
    if matched_keywords:
        score -= min(15 * len(matched_keywords), 40)
        flags.append(f"Suspicious keywords in domain: {', '.join(matched_keywords)}")
        
    # 2. High-Risk TLD Check
    high_risk_tlds = {
        "xyz": 25, "top": 25, "click": 20, "work": 20, "loan": 25,
        "info": 15, "bid": 20, "country": 20, "download": 20,
        "racing": 20, "gq": 30, "cf": 30, "tk": 30, "ml": 30,
        "ga": 30, "fit": 20, "buzz": 15, "club": 15, "live": 15
    }
    
    if tld in high_risk_tlds:
        deduction = high_risk_tlds[tld]
        score -= deduction
        flags.append(f"High-risk top-level domain (.{tld})")
        
    # 3. Brand Spoofing & Typosquatting Check
    target_brands = [
        "paypal", "netflix", "chase", "google", "microsoft", "apple",
        "amazon", "facebook", "instagram", "linkedin", "twitter",
        "steam", "binance", "coinbase", "bankofamerica", "wellsfargo"
    ]
    
    for brand in target_brands:
        # If the brand name is part of the SLD, but the SLD is not exactly the brand name
        if brand in sld and sld != brand:
            flags.append(f"Potential brand spoofing of '{brand}'")
            score -= 35
            break
            
        # Typosquatting check (close Levenshtein distance)
        if len(sld) >= 4 and abs(len(sld) - len(brand)) <= 2:
            dist = levenshtein_distance(sld, brand)
            if dist == 1: # 1 character difference (e.g. paypa1, netf1ix)
                flags.append(f"Potential typosquatting of brand '{brand}'")
                score -= 40
                break

    # Determine risk level based on the score
    if score >= 80:
        level = "LOW"
    elif score >= 50:
        level = "MEDIUM"
    else:
        level = "HIGH"
        
    return {
        "score": max(0, score),
        "level": level,
        "flags": flags
    }