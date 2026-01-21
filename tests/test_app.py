import unittest
from unittest.mock import MagicMock, patch
from graph_generator import generate_graph

class TestGraphGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_api = MagicMock()

    def test_generate_graph_success(self):
        # Mock API responses
        self.mock_api.get_worker_groups.return_value = {
            "items": [{"id": "default"}]
        }
        self.mock_api.get_sources.return_value = {
            "items": [
                {
                    "id": "in_syslog",
                    "disabled": False,
                    "connections": [{"output": "out_s3", "pipeline": "main"}],
                    "description": "Syslog Input"
                }
            ]
        }
        self.mock_api.get_destinations.return_value = {
            "items": [
                {
                    "id": "out_s3",
                    "description": "S3 Output"
                }
            ]
        }

        # Generate graph
        dot = generate_graph(self.mock_api)

        # Verify graph content
        source = dot.source
        self.assertIn("cluster_default", source)
        self.assertIn("default_in_syslog", source)
        self.assertIn("default_out_s3", source)
        self.assertIn("Syslog Input", source)
        self.assertIn('label=main', source)

    def test_generate_graph_no_groups(self):
        self.mock_api.get_worker_groups.return_value = {"items": []}
        with self.assertRaises(Exception) as context:
            generate_graph(self.mock_api)
        self.assertTrue("No worker groups found" in str(context.exception))

if __name__ == "__main__":
    unittest.main()
