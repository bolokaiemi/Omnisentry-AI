# ==========================================
# PHISHING CHECKER
# ==========================================

KNOWN_PHISHING_DOMAINS = {

    "fake-paypal-login.com",
    "secure-bank-login.net",
    "verify-account-now.org"
}


def check_phishing(domain: str):

    domain = domain.lower()

    return domain in KNOWN_PHISHING_DOMAINS