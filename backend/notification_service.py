from datetime import datetime

def send_push_notification(device_id: str, message: str, level: str):
    now = datetime.utcnow().isoformat()
    log_entry = f"[{now}] [PUSH NOTIFICATION] TO Device: {device_id} | LEVEL: {level} | MESSAGE: {message}"
    print(log_entry)
    
    # Mock writing notifications to a service log file
    try:
        with open("database/notifications.log", "a") as f:
            f.write(log_entry + "\n")
    except Exception:
        pass
        
    return True
