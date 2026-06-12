from src.website_analyzer import analyze_website as unified_analyze_website

# ==========================================
# DATA COLLECTION
# ==========================================

def collect_data(domain: str):
    report = unified_analyze_website(domain)
    
    # Return structure matching what data_route expects
    return {
        "domain": report["domain"],
        "registered": report["registered"],
        "age_days": report["age_days"],
        "ssl": report["ssl"],
        "reputation": report["reputation"]["level"] if isinstance(report["reputation"], dict) else report["reputation"],
        "ip_address": report["ip_address"],
        "country": report["country"],
        "city": report["city"],
        "latitude": report["latitude"],
        "longitude": report["longitude"]
    }


# ==========================================
# WEBSITE ANALYSIS (LEGACY)
# ==========================================

def analyze_website(domain: str):
    return unified_analyze_website(domain)
