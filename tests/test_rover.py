import unittest

from omnirover.rover_core import OmniRover


class TestOmniRover(unittest.TestCase):

    def setUp(self):
        self.rover = OmniRover()

    def test_rover_initialization(self):
        self.assertEqual(
            self.rover.status,
            "ACTIVE"
        )

    def test_safe_page_scan(self):

        page_data = """
        Welcome to our online store.
        Secure shopping experience.
        """

        result = self.rover.scan(page_data)

        self.assertIn(
            "threats",
            result
        )

        self.assertIn(
            "behavior",
            result
        )

        self.assertIn(
            "payment_check",
            result
        )

    def test_suspicious_page_scan(self):

        page_data = """
        urgent payment
        verify account
        crypto payment
        """

        result = self.rover.scan(page_data)

        self.assertGreater(
            result["threats"]["risk_score"],
            0
        )


if __name__ == "__main__":
    unittest.main()