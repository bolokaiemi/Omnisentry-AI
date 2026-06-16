# ==========================================
# OMMINSENTIRY AI
# THREAT INTELLIGENCE
# ==========================================

from src.phishing_checker import check_phishing
from src.scam_checker import check_scam


def threat_analysis(domain: str):

    phishing = check_phishing(domain)

    scam = check_scam(domain)

    threat_score = 0

    if phishing:
        threat_score += 50

    if scam:
        threat_score += 50

    return {

        "phishing_detected":
            phishing,

        "scam_detected":
            scam,

        "threat_score":
            threat_score
    }