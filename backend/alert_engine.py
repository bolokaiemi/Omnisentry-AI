import sqlite3
from datetime import datetime
from backend.event_store import store_threat_log
from backend.notification_service import send_push_notification
from backend.cybersec_dispatch import dispatch_critical_threat

ALERTS_DB = "database/alerts.db"

def process_report_for_alerts(device_id: str, report_data: dict):
    domain = report_data.get("domain", "unknown.com")
    risk_score = report_data.get("risk_score", 0)
    threats = report_data.get("threats", {})
    payment = report_data.get("payment_check", {})
    
    # 1. Log threats
    detected = threats.get("detected", [])
    for threat in detected:
        severity = "HIGH" if risk_score >= 70 else "MEDIUM"
        store_threat_log(device_id, domain, f"Keyword: {threat}", severity)
        
    if payment.get("payment_detected", False):
        severity = "CRITICAL" if payment.get("suspicious", False) else "MEDIUM"
        store_threat_log(device_id, domain, "Payment Fields Collected", severity)
        
    # 2. Trigger Alerts for severe items
    if risk_score >= 70 or payment.get("suspicious", False):
        level = "CRITICAL" if risk_score >= 80 else "HIGH"
        msg = f"Critical threat detected on {domain}. Risk Score: {risk_score}."
        if payment.get("suspicious", False):
            msg += " Suspicious payment request flagged."
            
        store_alert(device_id, level, msg)
        send_push_notification(device_id, msg, level)
        dispatch_critical_threat(device_id, "Phishing/Fraud", msg)
        
    elif risk_score >= 40:
        level = "MEDIUM"
        msg = f"Potential threat scan on {domain}. Risk Score: {risk_score}."
        store_alert(device_id, level, msg)

def store_alert(device_id: str, level: str, message: str):
    conn = sqlite3.connect(ALERTS_DB)
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO alerts (device_id, level, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (device_id, level, message, now))
    
    conn.commit()
    conn.close()
    return True

def get_recent_alerts(limit=10):
    conn = sqlite3.connect(ALERTS_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    
    alerts = []
    for row in rows:
        alerts.append({
            "id": row["id"],
            "device_id": row["device_id"],
            "level": row["level"],
            "message": row["message"],
            "timestamp": row["timestamp"]
        })
        
    conn.close()
    return alerts
