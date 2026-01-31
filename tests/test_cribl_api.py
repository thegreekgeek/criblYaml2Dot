import unittest
from unittest.mock import MagicMock, patch
from cribl_api import CriblAPI

class TestCriblAPI(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://mock-cribl:9000"
        self.api = CriblAPI(base_url=self.base_url, token="mock-token")
        # Mock the session object directly
        self.api.session = MagicMock()
        self.api.session.headers = {"Content-Type": "application/json", "Authorization": "Bearer mock-token"}

    def test_get_worker_groups(self):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": "default"}]}
        self.api.session.get.return_value = mock_response

        # Call the method
        groups = self.api.get_worker_groups()

        # Assertions
        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/master/groups"
        )
        self.assertEqual(groups, {"items": [{"id": "default"}]})

    def test_get_sources(self):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        self.api.session.get.return_value = mock_response

        self.api.get_sources(group_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/inputs"
        )

    def test_get_destinations(self):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        self.api.session.get.return_value = mock_response

        self.api.get_destinations(group_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/outputs"
        )

    def test_get_pipelines(self):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        self.api.session.get.return_value = mock_response

        self.api.get_pipelines(group_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/pipelines"
        )

if __name__ == '__main__':
    unittest.main()
