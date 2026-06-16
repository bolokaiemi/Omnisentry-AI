from datetime import datetime


KNOWN_PHISHING_DOMAINS = [

    "secure-login-check.net",
    "paypal-security-check.com",
    "verify-account-now.org",
    "bank-login-update.net"

]


def get_phishing_feed():

    return {

        "success": True,

        "timestamp":
            datetime.utcnow().isoformat(),

        "count":
            len(KNOWN_PHISHING_DOMAINS),

        "domains":
            KNOWN_PHISHING_DOMAINS
    }


def is_phishing_domain(domain: str):

    domain = domain.lower()

    return domain in KNOWN_PHISHING_DOMAINS