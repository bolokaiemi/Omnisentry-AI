import unittest

from omnirover.payment_guard import (
    check_payment_page
)

from omnirover.threat_scanner import (
    scan_page
)


class TestPaymentThreat(unittest.TestCase):

    # ======================================
    # PAYMENT GUARD TESTS
    # ======================================

    def test_payment_detection(self):

        page_data = """
        Enter your credit card number
        Enter CVV
        """

        result = check_payment_page(
            page_data
        )

        self.assertTrue(
            result["payment_detected"]
        )

        self.assertIn(
            "credit card",
            result["fields"]
        )

    def test_suspicious_payment_page(self):

        page_data = """
        Unverified merchant
        Enter bank transfer now
        """

        result = check_payment_page(
            page_data
        )

        self.assertTrue(
            result["suspicious"]
        )

    def test_safe_non_payment_page(self):

        page_data = """
        Welcome to our company homepage.
        Learn about our services.
        """

        result = check_payment_page(
            page_data
        )

        self.assertFalse(
            result["payment_detected"]
        )

    # ======================================
    # THREAT SCANNER TESTS
    # ======================================

    def test_safe_page_threat_score(self):

        page_data = """
        Welcome to official company website.
        """

        result = scan_page(
            page_data
        )

        self.assertEqual(
            result["risk_score"],
            0
        )

        self.assertEqual(
            len(result["detected"]),
            0
        )

    def test_detect_urgent_payment(self):

        page_data = """
        urgent payment required
        """

        result = scan_page(
            page_data
        )

        self.assertGreater(
            result["risk_score"],
            0
        )

        self.assertIn(
            "urgent payment",
            result["detected"]
        )

    def test_detect_multiple_threats(self):

        page_data = """
        urgent payment
        verify account
        send money now
        crypto payment
        gift card
        """

        result = scan_page(
            page_data
        )

        self.assertEqual(
            len(result["detected"]),
            5
        )

        self.assertEqual(
            result["risk_score"],
            100
        )

    # ======================================
    # COMBINED PAYMENT + THREAT TEST
    # ======================================

    def test_payment_and_threat_combined(self):

        page_data = """
        urgent payment
        verify account
        Enter credit card
        Enter CVV
        Unverified merchant
        """

        payment_result = check_payment_page(
            page_data
        )

        threat_result = scan_page(
            page_data
        )

        self.assertTrue(
            payment_result["payment_detected"]
        )

        self.assertTrue(
            payment_result["suspicious"]
        )

        self.assertGreater(
            threat_result["risk_score"],
            0
        )


if __name__ == "__main__":
    unittest.main()