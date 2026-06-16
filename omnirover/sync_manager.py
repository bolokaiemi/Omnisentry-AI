import requests

class SyncManager:
    def __init__(self, backend_url="http://127.0.0.1:8000"):
        self.backend_url = backend_url
        self.connected = False

    def connect(self, device_id, platform):
        try:
            response = requests.post(
                f"{self.backend_url}/api/device/register",
                json={"device_id": device_id, "platform": platform},
                timeout=5
            )
            if response.status_code == 200:
                self.connected = True
                return True
        except Exception as e:
            print(f"Failed to connect/register device: {e}")
        return False

    def sync(self, payload):
        # Keeps original method signature compatibility for existing test assertions
        if not self.connected:
            return {
                "success": False,
                "message": "Not connected"
            }
        
        device_id = payload.get("device_id", "DEV_ROVER")
        settings = payload.get("settings", {})
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/device/status",
                json={
                    "device_id": device_id,
                    "settings": settings
                },
                timeout=5
            )
            if response.status_code == 200:
                return {
                    "success": True,
                    "payload": payload
                }
        except Exception as e:
            print(f"Failed to sync settings: {e}")
            
        return {
            "success": False,
            "message": "Sync endpoint error"
        }
