import sqlite3
import json
from datetime import datetime

REPORTS_DB = "database/reports.db"
THREAT_LOGS_DB = "database/threat_logs.db"
DEVICES_DB = "database/devices.db"
ALERTS_DB = "database/alerts.db"

def store_report(device_id: str, domain: str, risk_score: int, status: str, threats: list, timestamp: str = None):
    conn = sqlite3.connect(REPORTS_DB)
    cursor = conn.cursor()
    
    if not timestamp:
        timestamp = datetime.utcnow().isoformat()
    threats_json = json.dumps(threats)
    
    cursor.execute("""
        INSERT INTO reports (device_id, domain, risk_score, status, threats, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (device_id, domain, risk_score, status, threats_json, timestamp))
    
    conn.commit()
    conn.close()
    return True

def store_threat_log(device_id: str, domain: str, threat: str, severity: str):
    conn = sqlite3.connect(THREAT_LOGS_DB)
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO threat_logs (device_id, domain, threat, severity, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (device_id, domain, threat, severity, now))
    
    conn.commit()
    conn.close()
    return True

def get_recent_reports(limit=10):
    conn = sqlite3.connect(REPORTS_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reports ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    
    reports = []
    for row in rows:
        reports.append({
            "id": row["id"],
            "device_id": row["device_id"],
            "domain": row["domain"],
            "risk_score": row["risk_score"],
            "status": row["status"],
            "threats": json.loads(row["threats"] or "[]"),
            "timestamp": row["timestamp"]
        })
        
    conn.close()
    return reports

def get_recent_threat_logs(limit=10):
    conn = sqlite3.connect(THREAT_LOGS_DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM threat_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    
    threats = []
    for row in rows:
        threats.append({
            "id": row["id"],
            "device_id": row["device_id"],
            "domain": row["domain"],
            "threat": row["threat"],
            "severity": row["severity"],
            "timestamp": row["timestamp"]
        })
        
    conn.close()
    return threats

def get_stats():
    # Helper to count total records in databases
    stats = {
        "threats": 0,
        "warnings": 0,
        "highrisk": 0,
        "devices": 0,
        "domains": 0
    }
    
    # 1. Total threats
    try:
        conn = sqlite3.connect(THREAT_LOGS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM threat_logs")
        stats["threats"] = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass
        
    # 2. Total warnings (alerts)
    try:
        conn = sqlite3.connect(ALERTS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM alerts")
        stats["warnings"] = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass
        
    # 3. High risk events (reports with risk score >= 70)
    try:
        conn = sqlite3.connect(REPORTS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM reports WHERE risk_score >= 70")
        stats["highrisk"] = cursor.fetchone()[0]
        
        # 4. Total domains scanned
        cursor.execute("SELECT COUNT(DISTINCT domain) FROM reports")
        stats["domains"] = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass
        
    # 5. Connected devices
    try:
        conn = sqlite3.connect(DEVICES_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM devices")
        stats["devices"] = cursor.fetchone()[0]
        conn.close()
    except Exception:
        pass
        
    return stats
