import unittest
from unittest.mock import MagicMock, patch
from cribl_api import CriblAPI
import requests

class TestCriblAPI(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://mock-api:9000"

    def test_init_with_token(self):
        token = "test-token"
        api = CriblAPI(base_url=self.base_url, token=token)
        self.assertEqual(api.base_url, self.base_url)
        self.assertEqual(api.headers["Authorization"], f"Bearer {token}")

    @patch("cribl_api.requests.post")
    def test_init_with_credentials(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "login-token"}
        mock_response.status_code = 200

        # Capture headers at call time
        captured_headers = []
        def side_effect(*args, **kwargs):
            if kwargs.get('headers'):
                captured_headers.append(kwargs.get('headers').copy())
            return mock_response

        mock_post.side_effect = side_effect

        api = CriblAPI(base_url=self.base_url, username="user", password="password")

        self.assertEqual(api.base_url, self.base_url)
        self.assertEqual(api.headers["Authorization"], "login-token")

        self.assertEqual(mock_post.call_count, 1)
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], f"{self.base_url}/api/v1/auth/login")
        self.assertEqual(kwargs['json'], {"username": "user", "password": "password"})

        # Verify headers captured at call time (should not have Authorization yet)
        self.assertEqual(captured_headers[0], {'Content-Type': 'application/json'})

    @patch("cribl_api.requests.post")
    def test_login_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"token": "new-token"}
        mock_response.status_code = 200

        # Capture headers at call time
        captured_headers = []
        def side_effect(*args, **kwargs):
            if kwargs.get('headers'):
                captured_headers.append(kwargs.get('headers').copy())
            return mock_response

        mock_post.side_effect = side_effect

        api = CriblAPI(base_url=self.base_url)
        api.login("user", "pass")

        self.assertEqual(api.headers["Authorization"], "new-token")

        self.assertEqual(mock_post.call_count, 1)
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], f"{self.base_url}/api/v1/auth/login")
        self.assertEqual(kwargs['json'], {"username": "user", "password": "pass"})

        self.assertEqual(captured_headers[0], {'Content-Type': 'application/json'})

    @patch("cribl_api.requests.post")
    def test_login_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Login failed")

        api = CriblAPI(base_url=self.base_url)
        with self.assertRaises(requests.exceptions.RequestException):
            api.login("user", "pass")

    @patch("cribl_api.requests.get")
    def test_get_worker_groups(self, mock_get):
        mock_response = MagicMock()
        expected_data = {"items": [{"id": "default"}]}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = CriblAPI(base_url=self.base_url, token="token")
        result = api.get_worker_groups()

        self.assertEqual(result, expected_data)
        # Using assert_called_with works here because we don't modify headers after this call in a way that affects this check
        # But we must be careful if we reuse the api object and modify headers.
        # Here we initialized with token, so headers has Authorization.
        # And get_worker_groups doesn't modify headers.

        mock_get.assert_called_with(
            f"{self.base_url}/api/v1/groups",
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer token'}
        )

    @patch("cribl_api.requests.get")
    def test_get_sources(self, mock_get):
        mock_response = MagicMock()
        expected_data = {"items": [{"id": "in_syslog"}]}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = CriblAPI(base_url=self.base_url, token="token")
        result = api.get_sources("default")

        self.assertEqual(result, expected_data)
        mock_get.assert_called_with(
            f"{self.base_url}/api/v1/groups/default/sources",
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer token'}
        )

    @patch("cribl_api.requests.get")
    def test_get_destinations(self, mock_get):
        mock_response = MagicMock()
        expected_data = {"items": [{"id": "out_s3"}]}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = CriblAPI(base_url=self.base_url, token="token")
        result = api.get_destinations("default")

        self.assertEqual(result, expected_data)
        mock_get.assert_called_with(
            f"{self.base_url}/api/v1/groups/default/destinations",
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer token'}
        )

    @patch("cribl_api.requests.get")
    def test_get_pipelines(self, mock_get):
        mock_response = MagicMock()
        expected_data = {"items": [{"id": "main"}]}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = CriblAPI(base_url=self.base_url, token="token")
        result = api.get_pipelines("default")

        self.assertEqual(result, expected_data)
        mock_get.assert_called_with(
            f"{self.base_url}/api/v1/groups/default/pipelines",
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer token'}
        )

    @patch("cribl_api.requests.get")
    def test_get_request_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        api = CriblAPI(base_url=self.base_url, token="token")
        with self.assertRaises(requests.exceptions.RequestException):
            api.get_worker_groups()

    @patch("cribl_api.requests.get")
    def test_json_decode_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError("msg", "doc", 0)
        mock_response.status_code = 200
        mock_response.text = "Not JSON"
        mock_get.return_value = mock_response

        api = CriblAPI(base_url=self.base_url, token="token")

        with self.assertRaises(requests.exceptions.JSONDecodeError):
            api.get_worker_groups()

if __name__ == '__main__':
    unittest.main()
