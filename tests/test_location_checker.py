
# ==========================================
# TEST LOCATION CHECKER
# ==========================================

from src.location_checker import get_location


def test_location_lookup():

    result = get_location(
        "google.com"
    )

    assert isinstance(
        result,
        dict
    )

    assert "ip_address" in result

    assert "country" in result

    assert "city" in result

    assert "latitude" in result

    assert "longitude" in result

