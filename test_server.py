"""Test for coders boost app."""
import unittest
import app


class ServerTests(unittest.TestCase):
    """Tests for my site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.app.test_client()
        app.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"Boost", result.data)

if __name__ == "__main__":
    unittest.main()