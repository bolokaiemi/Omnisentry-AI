import unittest

from omnirover.payment_guard import (
    check_payment_page
)


class TestPaymentGuard(unittest.TestCase):

    def test_detect_payment_fields(self):

        page_data = """
        Enter credit card
        Enter CVV
        """

        result = check_payment_page(
            page_data
        )

        self.assertTrue(
            result["payment_detected"]
        )

    def test_detect_suspicious_payment(self):

        page_data = """
        Unverified merchant.
        Enter credit card now.
        """

        result = check_payment_page(
            page_data
        )

        self.assertTrue(
            result["suspicious"]
        )

    def test_safe_page(self):

        page_data = """
        Welcome to homepage
        """

        result = check_payment_page(
            page_data
        )

        self.assertFalse(
            result["payment_detected"]
        )


if __name__ == "__main__":
    unittest.main()