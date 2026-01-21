import unittest
from unittest.mock import MagicMock, patch
from cribl_api import CriblAPI

class TestCriblAPI(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://mock-cribl:9000"
        self.api = CriblAPI(base_url=self.base_url, token="mock-token")

    @patch('requests.get')
    def test_get_worker_groups(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": "default"}]}
        mock_get.return_value = mock_response

        # Call the method
        groups = self.api.get_worker_groups()

        # Assertions
        mock_get.assert_called_with(
            f"{self.base_url}/api/v1/master/groups",
            headers={"Content-Type": "application/json", "Authorization": "Bearer mock-token"}
        )
        self.assertEqual(groups, {"items": [{"id": "default"}]})

    @patch('requests.get')
    def test_get_sources(self, mock_get):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        self.api.get_sources(group_id)

        mock_get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/inputs",
            headers={"Content-Type": "application/json", "Authorization": "Bearer mock-token"}
        )

    @patch('requests.get')
    def test_get_destinations(self, mock_get):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        self.api.get_destinations(group_id)

        mock_get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/outputs",
            headers={"Content-Type": "application/json", "Authorization": "Bearer mock-token"}
        )

    @patch('requests.get')
    def test_get_pipelines(self, mock_get):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        self.api.get_pipelines(group_id)

        mock_get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/pipelines",
            headers={"Content-Type": "application/json", "Authorization": "Bearer mock-token"}
        )

if __name__ == '__main__':
    unittest.main()
