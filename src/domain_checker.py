import whois
import socket
from datetime import datetime

def parse_date(date_val):
    if not date_val:
        return None
    if isinstance(date_val, list):
        for item in date_val:
            parsed = parse_date(item)
            if parsed:
                return parsed
        return None
    if isinstance(date_val, datetime):
        return date_val
    # If it is a string, try parsing common formats
    if isinstance(date_val, str):
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d",
            "%d-%b-%Y",
            "%Y.%m.%d",
        ):
            try:
                return datetime.strptime(date_val.strip(), fmt)
            except ValueError:
                continue
    return None

def check_domain(domain):
    # Secondary check: does it resolve to an IP?
    dns_resolves = False
    try:
        socket.gethostbyname(domain)
        dns_resolves = True
    except Exception:
        pass

    try:
        w = whois.whois(domain)
        
        # If registrar is None and creation_date is None, it is highly likely unregistered
        creation = parse_date(w.creation_date)
        expiration = parse_date(w.expiration_date)
        updated = parse_date(w.updated_date)
        
        registrar = w.registrar
        if isinstance(registrar, list):
            registrar = registrar[0] if registrar else None
            
        status = w.status
        if isinstance(status, list):
            status = ", ".join([str(s) for s in status])
            
        name_servers = w.name_servers
        if not name_servers:
            name_servers = []
        elif not isinstance(name_servers, list):
            name_servers = [name_servers]
            
        # Clean name servers
        name_servers = [str(ns).strip().lower() for ns in name_servers if ns]

        if not creation and not registrar and not dns_resolves:
            return {
                "registered": False,
                "age_days": 0,
                "registrar": None,
                "creation_date": None,
                "expiration_date": None,
                "updated_date": None,
                "name_servers": [],
                "status": None
            }

        age_days = 0
        if creation:
            age_days = (datetime.now() - creation).days
            # Ensure age_days is not negative
            age_days = max(0, age_days)

        return {
            "registered": True,
            "age_days": age_days,
            "registrar": registrar or "Unknown",
            "creation_date": creation.strftime("%Y-%m-%d") if creation else "Unknown",
            "expiration_date": expiration.strftime("%Y-%m-%d") if expiration else "Unknown",
            "updated_date": updated.strftime("%Y-%m-%d") if updated else "Unknown",
            "name_servers": name_servers,
            "status": status or "Active"
        }

    except Exception:
        # If whois fail but DNS resolves, we can assume it's registered but details are hidden/unparseable
        if dns_resolves:
            return {
                "registered": True,
                "age_days": 365,  # Assume 1 year if details are unknown but it resolves
                "registrar": "Unknown (WHOIS Redacted)",
                "creation_date": "Unknown",
                "expiration_date": "Unknown",
                "updated_date": "Unknown",
                "name_servers": [],
                "status": "Active"
            }
            
        return {
            "registered": False,
            "age_days": 0,
            "registrar": None,
            "creation_date": None,
            "expiration_date": None,
            "updated_date": None,
            "name_servers": [],
            "status": None
        }