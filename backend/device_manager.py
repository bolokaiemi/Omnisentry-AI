import sqlite3
from datetime import datetime

DATABASE_PATH = "database/devices.db"

def register_device(device_id: str, platform: str):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO devices (device_id, platform, status, last_sync)
        VALUES (?, ?, 'ONLINE', ?)
        ON CONFLICT(device_id) DO UPDATE SET
            platform = excluded.platform,
            status = 'ONLINE',
            last_sync = excluded.last_sync
    """, (device_id, platform, now))
    
    conn.commit()
    conn.close()
    return True

def update_device_status(device_id: str, settings: dict):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat()
    parental = 1 if settings.get("parental_control_enabled", False) else 0
    payment = 1 if settings.get("payment_guard_enabled", False) else 0
    
    cursor.execute("""
        UPDATE devices
        SET last_sync = ?,
            parental_control_enabled = ?,
            payment_guard_enabled = ?,
            status = 'ONLINE'
        WHERE device_id = ?
    """, (now, parental, payment, device_id))
    
    conn.commit()
    conn.close()
    return True

def get_devices():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM devices ORDER BY last_sync DESC")
    rows = cursor.fetchall()
    
    devices = []
    for row in rows:
        devices.append({
            "id": row["id"],
            "device_id": row["device_id"],
            "user_id": row["user_id"],
            "platform": row["platform"],
            "status": row["status"],
            "last_sync": row["last_sync"],
            "parental_control_enabled": bool(row["parental_control_enabled"]),
            "payment_guard_enabled": bool(row["payment_guard_enabled"])
        })
        
    conn.close()
    return devices
