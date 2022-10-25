"""Test for coders boost app."""

import unittest
import server


class ServerTests(unittest.TestCase):
    """Tests for my site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"Welcome!", result.data)

if __name__ == "__main__":
    unittest.main()