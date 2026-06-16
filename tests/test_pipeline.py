import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app import app
import sqlite3

def run_e2e_pipeline_verification():
    print("=" * 60)
    print("E2E PIPELINE INTEGRATION TEST")
    print("=" * 60)
    
    client = TestClient(app)
    
    # 1. Register a test device
    print("[+] Step 1: Registering mobile device...")
    reg_response = client.post("/api/device/register", json={
        "device_id": "Test-Pipeline-Device",
        "platform": "Android"
    })
    print(f"    Status: {reg_response.status_code}")
    print(f"    Body: {reg_response.json()}")
    assert reg_response.status_code == 200
    
    # Verify in DB
    conn = sqlite3.connect("database/devices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE device_id = 'Test-Pipeline-Device'")
    row = cursor.fetchone()
    conn.close()
    print(f"    Database verification: Found device = {row is not None}")
    assert row is not None
    
    # 2. Update status and features
    print("\n[+] Step 2: Syncing device settings...")
    sync_response = client.post("/api/device/status", json={
        "device_id": "Test-Pipeline-Device",
        "settings": {
            "parental_control_enabled": True,
            "payment_guard_enabled": True
        }
    })
    print(f"    Status: {sync_response.status_code}")
    print(f"    Body: {sync_response.json()}")
    assert sync_response.status_code == 200
    
    # Verify features in DB
    conn = sqlite3.connect("database/devices.db")
    cursor = conn.cursor()
    cursor.execute("SELECT parental_control_enabled, payment_guard_enabled FROM devices WHERE device_id = 'Test-Pipeline-Device'")
    row = cursor.fetchone()
    conn.close()
    print(f"    Database verification: Parental={bool(row[0])}, PaymentGuard={bool(row[1])}")
    assert bool(row[0]) is True
    assert bool(row[1]) is True
    
    # 3. Simulate threat trigger
    print("\n[+] Step 3: Triggering mobile scan pipeline simulation...")
    sim_response = client.post("/api/simulator/trigger", json={
        "device_id": "Test-Pipeline-Device",
        "platform": "Android",
        "domain": "netflix-rewards-phishing.com",
        "page_content": "Unverified merchant. Urgent payment required to verify account now. Please enter your credit card number and CVV."
    })
    print(f"    Status: {sim_response.status_code}")
    print(f"    Scan Risk Score: {sim_response.json()['scan_result']['risk_score']}")
    assert sim_response.status_code == 200
    
    # 4. Check if reports are logged
    print("\n[+] Step 4: Validating threat logs & reports in databases...")
    conn = sqlite3.connect("database/reports.db")
    cursor = conn.cursor()
    cursor.execute("SELECT domain, risk_score, status FROM reports WHERE device_id = 'Test-Pipeline-Device'")
    reports = cursor.fetchall()
    conn.close()
    print(f"    Report logs found in DB: {reports}")
    assert len(reports) > 0
    
    # Check if alerts are triggered
    conn = sqlite3.connect("database/alerts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT level, message FROM alerts WHERE device_id = 'Test-Pipeline-Device'")
    alerts = cursor.fetchall()
    conn.close()
    print(f"    Incidents alerts found in DB: {alerts}")
    assert len(alerts) > 0
    
    # 5. Fetch Dashboard API Stats
    print("\n[+] Step 5: Fetching Dashboard Stats endpoint...")
    stats_response = client.get("/api/dashboard/stats")
    print(f"    Status: {stats_response.status_code}")
    print(f"    Stats body: {stats_response.json()}")
    assert stats_response.status_code == 200
    
    print("\n" + "=" * 60)
    print("ALL E2E PIPELINE TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_e2e_pipeline_verification()
