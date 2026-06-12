
# ==========================================
# TEST DOMAIN CHECKER
# ==========================================

from src.domain_checker import check_domain


def test_google_domain():

    result = check_domain(
        "google.com"
    )

    assert isinstance(
        result,
        dict
    )

    assert "registered" in result

    assert "age_days" in result


def test_invalid_domain():

    result = check_domain(
        "this-domain-does-not-exist-123456.com"
    )

    assert isinstance(
        result,
        dict
    )

