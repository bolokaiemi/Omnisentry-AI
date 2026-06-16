from datetime import datetime

def dispatch_critical_threat(device_id: str, threat_type: str, details: str):
    now = datetime.utcnow().isoformat()
    dispatch_entry = f"[{now}] [SOC DISPATCH] [CRITICAL] Device: {device_id} | Type: {threat_type} | Details: {details}"
    print(dispatch_entry)
    
    # Mock writing dispatch events to a cybersecurity dispatch log file
    try:
        with open("database/cybersec_dispatch.log", "a") as f:
            f.write(dispatch_entry + "\n")
    except Exception as e:
        print(f"Failed to write cybersec dispatch log: {e}")
        
    return True
