from datetime import datetime


KNOWN_SCAM_DOMAINS = [

    "fake-bank-login.com",
    "free-money-now.net",
    "crypto-fast-profit.org",
    "winner-prize-claim.com"

]


def collect_scam_feeds():

    return {

        "success": True,

        "timestamp":
            datetime.utcnow().isoformat(),

        "total":
            len(KNOWN_SCAM_DOMAINS),

        "domains":
            KNOWN_SCAM_DOMAINS
    }


def is_known_scam(domain: str):

    domain = domain.lower()

    return domain in KNOWN_SCAM_DOMAINS