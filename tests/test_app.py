import unittest
from app import app, quotes
import json
from parameterized import parameterized


class TestQuotesApp(unittest.TestCase):

    def setUp(self):
        """Initialize for each test"""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "random_value"
        self.client = app.test_client()

    def test_home_page(self):
        """Test if the home page loads successfully with a random quote."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data)  # Check for Welcome text
        self.assertIn(b"quote", response.data)  # Check for quote text

    @parameterized.expand([
        ("start", 0),
        ("inside", 5),
        ("wrapping", len(quotes)),
    ])
    def test_next_quote(self, test_name, current_id):
        """Test if the /next endpoint returns the correct next quote.
            Also test if it wraps around when max has been reached
        """
        response = self.client.get(f'/next?id={current_id}')
        self.assertEqual(response.status_code, 200)

        # Parse JSON response and check content (keys only)
        data = json.loads(response.data)
        expected_id = (current_id + 1) % len(quotes)
        self.assertEqual(data["id"], expected_id)
        self.assertIn("quote", data)

    def test_random_quote(self):
        """Test if the /random endpoint returns a random quote."""
        response = self.client.get('/random')
        self.assertEqual(response.status_code, 200)

        # Parse JSON response and check content (keys only)
        data = json.loads(response.data)
        self.assertIn("quote", data)
        self.assertIn("author", data)

    def test_login(self):
        """Test if the login endpoint successfully updates the user's name."""
        response = self.client.post(
            '/login',
            data=json.dumps({"name": "Vio"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Parse JSON response
        data = json.loads(response.data)
        self.assertEqual(data["name"], "Vio")


if __name__ == '__main__':
    unittest.main()