import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_cached_api_client')
    @patch('app.generate_graph')
    def test_index_success(self, mock_generate_graph, mock_get_client):
        # Mock the API client
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Mock the graph generation
        mock_dot = MagicMock()
        mock_dot.pipe.return_value = b"<svg>...</svg>"
        mock_generate_graph.return_value = mock_dot

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<svg>...</svg>", response.data)

    @patch('app.get_cached_api_client')
    def test_index_error(self, mock_get_client):
        # Mock an exception
        mock_get_client.side_effect = Exception("API connection failed")

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # It renders error.html, which is 200 OK usually
        self.assertIn(b"API connection failed", response.data)

if __name__ == '__main__':
    unittest.main()
