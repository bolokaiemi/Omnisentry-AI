import unittest

# Adjust import based on your actual file location:
# from omnipop.phishing_detector import detect_phishing
# OR
# from omnirover.phishing_detector import detect_phishing

from src.omnipop.phishing_detector import detect_phishing


class TestPhishingDetector(unittest.TestCase):

    def test_safe_website(self):

        page_data = """
        Welcome to our official company website.
        Secure login portal with verified SSL.
        """

        result = detect_phishing(page_data)

        self.assertFalse(
            result["is_phishing"]
        )

    def test_fake_bank_page(self):

        page_data = """
        Verify account immediately.
        Enter bank password now.
        """

        result = detect_phishing(page_data)

        self.assertTrue(
            result["is_phishing"]
        )

    def test_credential_harvest(self):

        page_data = """
        Login now with password.
        Enter OTP.
        Verify account.
        """

        result = detect_phishing(page_data)

        self.assertTrue(
            result["is_phishing"]
        )

        self.assertGreater(
            result["phishing_score"],
            0
        )

    def test_payment_scam(self):

        page_data = """
        Send money now.
        Crypto payment only.
        """

        result = detect_phishing(page_data)

        self.assertTrue(
            result["is_phishing"]
        )

    def test_multiple_phishing_signals(self):

        page_data = """
        Verify account now.
        Enter credit card.
        Send money immediately.
        Password required.
        OTP required.
        """

        result = detect_phishing(page_data)

        self.assertTrue(
            result["is_phishing"]
        )

        self.assertGreaterEqual(
            result["phishing_score"],
            80
        )


if __name__ == "__main__":
    unittest.main()