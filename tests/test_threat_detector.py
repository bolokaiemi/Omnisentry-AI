import pytest

from src.omnipop.threat_detector import (
    detect_threat
)


def test_detect_threat_payment_request():

    content = """
    Please enter your credit card
    information to continue.
    """

    result = detect_threat(
        content
    )

    assert "PAYMENT_REQUEST" in result[
        "threats"
    ]

    assert result[
        "risk_score"
    ] > 0


def test_detect_threat_phishing():

    content = """
    Login now.
    Verify account immediately.
    Enter password.
    """

    result = detect_threat(
        content
    )

    assert "PHISHING" in result[
        "threats"
    ]


def test_detect_threat_urgency_language():

    content = """
    Act now.
    Limited time offer.
    Verify immediately.
    """

    result = detect_threat(
        content
    )

    assert "URGENCY_LANGUAGE" in result[
        "threats"
    ]


def test_detect_threat_combined():

    content = """
    Act now.

    Verify account immediately.

    Enter password.

    Submit your credit card.
    """

    result = detect_threat(
        content
    )

    assert len(
        result["threats"]
    ) >= 2

    assert result[
        "risk_score"
    ] >= 60


def test_detect_threat_safe_content():

    content = """
    Welcome to our website.

    Browse our products.

    Contact support if needed.
    """

    result = detect_threat(
        content
    )

    assert result[
        "threats"
    ] == []

    assert result[
        "risk_score"
    ] == 0