import sqlite3
import os

def initialize_database():
    os.makedirs("database", exist_ok=True)

    # USERS
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

    # ALERTS
    conn = sqlite3.connect("database/alerts.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            level TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

    # DEVICES
    conn = sqlite3.connect("database/devices.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE,
            user_id INTEGER,
            platform TEXT,
            status TEXT,
            last_sync TEXT,
            parental_control_enabled INTEGER DEFAULT 0,
            payment_guard_enabled INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

    # REPORTS
    conn = sqlite3.connect("database/reports.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            domain TEXT,
            risk_score INTEGER,
            status TEXT,
            threats TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

    # THREAT LOGS
    conn = sqlite3.connect("database/threat_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS threat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            domain TEXT,
            threat TEXT,
            severity TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

    # FEEDBACK / REVIEWS
    conn = sqlite3.connect("database/feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating INTEGER,
            comment TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()

    # Seed initial reviews if empty
    cursor.execute("SELECT COUNT(*) FROM feedback")
    if cursor.fetchone()[0] == 0:
        seed_reviews = [
            ("Marcus K.", 5, "Omminsentiry AI caught a suspicious domain posing as my bank. Saved me from a major phishing scam!", "2026-06-12T14:32:00Z"),
            ("Elena R.", 5, "The real-time Threat Map and mobile notifications are super responsive. Extremely helpful cybersecurity project.", "2026-06-13T09:15:00Z"),
            ("Sarah L.", 4, "Great UI design and fast scans! Love the trust score concept. Excited to see where this platform goes.", "2026-06-14T18:45:00Z"),
            ("Tariq A.", 5, "A crucial tool for checking domain age and SSL certificates before doing any transactions online. Highly recommend!", "2026-06-15T11:20:00Z"),
            ("Sophia W.", 5, "The Random Forest classifier is highly accurate in threat prediction. This platform is a must-have safety layer.", "2026-06-15T20:05:00Z")
        ]
        cursor.executemany("""
            INSERT INTO feedback (name, rating, comment, timestamp)
            VALUES (?, ?, ?, ?)
        """, seed_reviews)
        conn.commit()

    conn.close()

    print("Database initialization complete.")

if __name__ == "__main__":
    initialize_database()

