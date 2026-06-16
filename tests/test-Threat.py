import unittest

from omnirover.threat_scanner import scan_page


class TestThreatScanner(unittest.TestCase):

    def test_safe_page(self):

        page_data = """
        Welcome to our official website.
        Secure browsing experience.
        """

        result = scan_page(page_data)

        self.assertEqual(
            result["risk_score"],
            0
        )

        self.assertEqual(
            len(result["detected"]),
            0
        )

    def test_urgent_payment_detection(self):

        page_data = """
        urgent payment required now
        """

        result = scan_page(page_data)

        self.assertGreater(
            result["risk_score"],
            0
        )

        self.assertIn(
            "urgent payment",
            result["detected"]
        )

    def test_verify_account_detection(self):

        page_data = """
        Please verify account immediately
        """

        result = scan_page(page_data)

        self.assertIn(
            "verify account",
            result["detected"]
        )

    def test_multiple_threats(self):

        page_data = """
        urgent payment
        verify account
        send money now
        crypto payment
        gift card
        """

        result = scan_page(page_data)

        self.assertEqual(
            len(result["detected"]),
            5
        )

        self.assertEqual(
            result["risk_score"],
            100
        )

    def test_crypto_payment_detection(self):

        page_data = """
        Payment accepted only via crypto payment
        """

        result = scan_page(page_data)

        self.assertIn(
            "crypto payment",
            result["detected"]
        )


if __name__ == "__main__":
    unittest.main()