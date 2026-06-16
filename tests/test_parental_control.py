import unittest

from omnirover.parental_control import parental_guard


class TestParentalControl(unittest.TestCase):

    def test_child_payment_block(self):

        result = parental_guard(
            age=12,
            action="payment"
        )

        self.assertFalse(
            result["allowed"]
        )

    def test_child_gambling_block(self):

        result = parental_guard(
            age=16,
            action="gambling"
        )

        self.assertFalse(
            result["allowed"]
        )

    def test_adult_payment_allowed(self):

        result = parental_guard(
            age=25,
            action="payment"
        )

        self.assertTrue(
            result["allowed"]
        )

    def test_safe_action_allowed(self):

        result = parental_guard(
            age=10,
            action="watch_video"
        )

        self.assertTrue(
            result["allowed"]
        )


if __name__ == "__main__":
    unittest.main()