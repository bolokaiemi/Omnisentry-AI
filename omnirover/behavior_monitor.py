
def monitor_behavior(page_data):

    threats = []

    risk_score = 0

    if "redirect_loop" in page_data:
        threats.append("Rapid Redirect")
        risk_score += 40

    if "fake_popup" in page_data:
        threats.append("Fake Popup")
        risk_score += 30

    if "clipboard_access" in page_data:
        threats.append("Clipboard Hijacking")
        risk_score += 30

    return {
        "suspicious": risk_score > 0,
        "risk_score": risk_score,
        "threats": threats
    }
