import json
import requests
from datetime import datetime
from omnirover.encrypted_channel import encrypt_data

def send_report(report, device_id, backend_url="http://127.0.0.1:8000"):
    report_payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "device_id": device_id,
        "report": report
    }
    serialized = json.dumps(report_payload)
    encrypted = encrypt_data(serialized)
    
    try:
        response = requests.post(
            f"{backend_url}/api/threat/report",
            json={"encrypted_payload": encrypted, "device_id": device_id},
            timeout=2
        )
        if response.status_code == 200:
            return True
    except Exception as e:
        print(f"Failed to send threat report to backend via HTTP: {e}")
        
    # In-process Fallback for testing / TestClient
    try:
        from backend.event_store import store_report
        from backend.alert_engine import process_report_for_alerts
        
        print(f"  [Fallback] Writing report directly to database for device: {device_id}")
        store_report(
            device_id=device_id,
            domain=report.get("domain", "unknown.com"),
            risk_score=report.get("risk_score", 0),
            status="FLAGGED" if report.get("risk_score", 0) >= 50 else "CLEAN",
            threats=report.get("threats", {}).get("detected", []),
            timestamp=report_payload["timestamp"]
        )
        process_report_for_alerts(device_id, report)
        return True
    except Exception as fallback_err:
        print(f"  [Fallback] Direct database logging failed: {fallback_err}")
        return False
