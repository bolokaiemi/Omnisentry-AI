import whois
from datetime import datetime

def check_domain(domain):

    try:
        w = whois.whois(domain)

        creation = w.creation_date

        if isinstance(creation, list):
            creation = creation[0]

        age_days = (datetime.now() - creation).days

        return {
            "registered": True,
            "age_days": age_days
        }

    except Exception:

        return {
            "registered": False,
            "age_days": 0
        }