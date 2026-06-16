from datetime import datetime


def create_report(
    domain,
    threats,
    risk_score
):

    return {

        "domain":
            domain,

        "threats":
            threats,

        "risk_score":
            risk_score,

        "timestamp":
            datetime.utcnow().isoformat()
    }