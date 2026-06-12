
# ==========================================
# TEST SSL CHECKER
# ==========================================

from src.ssl_checker import check_ssl


def test_ssl_google():

    result = check_ssl(
        "google.com"
    )

    assert isinstance(
        result,
        bool
    )


def test_ssl_invalid():

    result = check_ssl(
        "invalid-domain-test-123.com"
    )

    assert isinstance(
        result,
        bool
    )

