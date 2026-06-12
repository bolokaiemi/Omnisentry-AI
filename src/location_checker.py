import socket
import requests

def get_location(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        
        if ip_address in ("127.0.0.1", "0.0.0.0", "localhost"):
            return {
                "ip_address": ip_address,
                "country": "Localhost",
                "city": "Local Development",
                "latitude": 0.0,
                "longitude": 0.0,
                "isp": "Local Loopback",
                "asn": "N/A"
            }

        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "ip_address": ip_address,
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "latitude": data.get("lat"),
                    "longitude": data.get("lon"),
                    "isp": data.get("isp", "Unknown"),
                    "asn": data.get("as", "Unknown")
                }

        return {
            "ip_address": ip_address,
            "country": "Unknown",
            "city": "Unknown",
            "latitude": None,
            "longitude": None,
            "isp": "Unknown",
            "asn": "Unknown"
        }

    except Exception:
        return {
            "ip_address": None,
            "country": "Unknown",
            "city": "Unknown",
            "latitude": None,
            "longitude": None,
            "isp": "Unknown",
            "asn": "Unknown"
        }