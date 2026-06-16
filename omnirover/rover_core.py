from omnirover.threat_scanner import scan_page
from omnirover.behavior_monitor import monitor_behavior
from omnirover.payment_guard import check_payment_page
from omnirover.fraud_reporter import send_report

class OmniRover:
    def __init__(self, device_id="DEV_ROVER", platform="iOS", backend_url="http://127.0.0.1:8000"):
        self.device_id = device_id
        self.platform = platform
        self.backend_url = backend_url
        self.status = "ACTIVE"

    def scan(self, page_data, domain="unknown.com"):
        threats = scan_page(page_data)
        behavior = monitor_behavior(page_data)
        payment = check_payment_page(page_data)

        result = {
            "domain": domain,
            "threats": threats,
            "behavior": behavior,
            "payment_check": payment
        }

        # Calculate a combined risk score
        risk_score = threats.get("risk_score", 0)
        if payment.get("suspicious", False):
            risk_score = max(risk_score, 80)
        elif payment.get("payment_detected", False):
            risk_score = max(risk_score, 40)
        
        result["risk_score"] = risk_score

        # Automatically send report if threat is detected
        if risk_score > 30:
            send_report(result, self.device_id, self.backend_url)

        return result
