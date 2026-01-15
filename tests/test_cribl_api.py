import unittest
from unittest.mock import patch, MagicMock
from cribl_api import CriblAPI

class TestCriblAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://mock-url"
        self.api = CriblAPI(base_url=self.base_url)

    def test_init_with_token(self):
        token = "mock-token"
        api = CriblAPI(base_url=self.base_url, token=token)
        self.assertEqual(api.headers["Authorization"], f"Bearer {token}")

    @patch("requests.post")
    def test_login(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token": "new-token"}
        mock_post.return_value = mock_response

        self.api.login("user", "pass")

        # Verify that the Authorization header is set correctly.
        self.assertEqual(self.api.headers["Authorization"], "Bearer new-token")

    @patch("requests.get")
    def test_get_worker_groups(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        self.api.get_worker_groups()
        mock_get.assert_called_with(f"{self.base_url}/api/v1/groups", headers=self.api.headers)

    @patch("requests.get")
    def test_get_sources(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        self.api.get_sources("default")
        mock_get.assert_called_with(f"{self.base_url}/api/v1/groups/default/sources", headers=self.api.headers)

if __name__ == "__main__":
    unittest.main()
