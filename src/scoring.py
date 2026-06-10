def calculate_score(
    age_days,
    ssl_status,
    reputation
):

    score = 50

    if age_days > 365:
        score += 20

    if age_days > 1825:
        score += 20

    if ssl_status:
        score += 20

    if reputation == "HIGH":
        score -= 60

    return max(0, min(score, 100))