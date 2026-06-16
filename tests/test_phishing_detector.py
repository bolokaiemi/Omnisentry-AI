import pytest

from src.omnipop.phishing_detector import (
    detect_phishing
)


def test_detect_phishing_positive():

    content = """
    Please login to your account.
    Verify account immediately.
    Enter your password below.
    """

    result = detect_phishing(
        content
    )

    assert result["is_phishing"] is True

def test_detect_phishing_negative():

    content = """
    Welcome to our company website.
    Learn more about our products.
    Contact us for information.
    """

    result = detect_phishing(
        content
    )

    assert result["is_phishing"] is False


def test_detect_phishing_password_only():

    content = """
    Password policy information.
    """

    result = detect_phishing(
        content
    )

    assert result["is_phishing"] is False


def test_detect_phishing_multiple_keywords():

    content = """
    Login now.
    Verify account.
    Confirm account.
    Security code required.
    """

    result = detect_phishing(
        content
    )

    assert result["is_phishing"] is True