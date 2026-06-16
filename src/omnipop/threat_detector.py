from src.omnipop.payment_detector import detect_payment_request
from src.omnipop.phishing_detector import detect_phishing
from src.omnipop.behavior_analyzer import analyze_behavior


def detect_threat(content: str):

    threats = []

    if detect_payment_request(content):
        threats.append("PAYMENT_REQUEST")

    if detect_phishing(content)["is_phishing"]:
        threats.append("PHISHING")

    behavior = analyze_behavior(content)

    if behavior["urgency"]:
        threats.append("URGENCY_LANGUAGE")

    risk_score = len(threats) * 30

    return {
        "threats": threats,
        "risk_score": min(risk_score, 100)
    }