import unittest
from unittest.mock import MagicMock
from cribl_api import CriblAPI

class TestCriblAPI(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://mock-cribl:9000"
        self.api = CriblAPI(base_url=self.base_url, token="mock-token")
        # Mock the session object directly since CriblAPI uses self.session.get/post
        self.api.session = MagicMock()

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

    def test_get_source_status(self):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        self.api.session.get.return_value = mock_response

        self.api.get_source_status(group_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/status/inputs"
        )

    def test_get_destination_status(self):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        self.api.session.get.return_value = mock_response

        self.api.get_destination_status(group_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/status/outputs"
        )

    def test_get_pipeline_status(self):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": "main", "eps": 100.0}]}
        self.api.session.get.return_value = mock_response

        result = self.api.get_pipeline_status(group_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/status/pipelines"
        )
        self.assertEqual(result, {"items": [{"id": "main", "eps": 100.0}]})

    def test_get_pipeline_status_failure_graceful(self):
        """Test that pipeline status gracefully handles API errors."""
        group_id = "test-group"
        self.api.session.get.side_effect = Exception("API Error")

        result = self.api.get_pipeline_status(group_id)

        # Should return empty items on failure
        self.assertEqual(result, {"items": []})

    def test_get_source_health(self):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": "in_1", "error_rate": 2.0}]
        }
        self.api.session.get.return_value = mock_response

        result = self.api.get_source_health(group_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/health/inputs"
        )
        self.assertEqual(result, {"items": [{"id": "in_1", "error_rate": 2.0}]})

    def test_get_source_health_failure_graceful(self):
        """Test that source health gracefully handles API errors."""
        group_id = "test-group"
        self.api.session.get.side_effect = Exception("API Error")

        result = self.api.get_source_health(group_id)

        # Should return empty items on failure
        self.assertEqual(result, {"items": []})

    def test_get_destination_health(self):
        group_id = "test-group"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": "out_1", "error_rate": 1.5}]
        }
        self.api.session.get.return_value = mock_response

        result = self.api.get_destination_health(group_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/system/health/outputs"
        )
        self.assertEqual(result, {"items": [{"id": "out_1", "error_rate": 1.5}]})

    def test_get_destination_health_failure_graceful(self):
        """Test that destination health gracefully handles API errors."""
        group_id = "test-group"
        self.api.session.get.side_effect = Exception("API Error")

        result = self.api.get_destination_health(group_id)

        # Should return empty items on failure
        self.assertEqual(result, {"items": []})

    def test_get_pipeline_functions(self):
        """Test retrieving pipeline function details for complexity scoring."""
        group_id = "test-group"
        pipeline_id = "test-pipeline"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": pipeline_id,
            "functions": [
                {"name": "func1", "type": "regex"},
                {"name": "func2", "type": "lookup"},
                {"name": "func3", "type": "json"},
            ],
        }
        self.api.session.get.return_value = mock_response

        result = self.api.get_pipeline_functions(group_id, pipeline_id)

        self.api.session.get.assert_called_with(
            f"{self.base_url}/api/v1/m/{group_id}/pipelines/{pipeline_id}"
        )
        self.assertEqual(len(result.get("functions", [])), 3)
        self.assertEqual(result["id"], pipeline_id)

    def test_get_pipeline_functions_graceful_failure(self):
        """Test that pipeline functions gracefully handle API errors."""
        group_id = "test-group"
        pipeline_id = "test-pipeline"
        self.api.session.get.side_effect = Exception("Pipeline not found")

        result = self.api.get_pipeline_functions(group_id, pipeline_id)

        # Should return empty dict on failure for graceful degradation
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
