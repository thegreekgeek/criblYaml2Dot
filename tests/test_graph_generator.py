import unittest
from unittest.mock import MagicMock
from graph_generator import generate_graph

class TestGraphGenerator(unittest.TestCase):

    def test_generate_graph(self):
        # Mock API client
        mock_api_client = MagicMock()

        # Mock data
        mock_api_client.get_worker_groups.return_value = {
            "items": [{"id": "default"}]
        }
        mock_api_client.get_sources.return_value = {
            "items": [
                {
                    "id": "in_syslog",
                    "description": "Syslog Input",
                    "disabled": False,
                    "connections": [
                        {"output": "out_s3", "pipeline": "main"}
                    ]
                }
            ]
        }
        mock_api_client.get_destinations.return_value = {
            "items": [
                {
                    "id": "out_s3",
                    "description": "S3 Output",
                    "disabled": False
                }
            ]
        }

        # Generate graph
        dot = generate_graph(mock_api_client)

        # Basic assertions on the generated graph content
        source_code = dot.source
        self.assertIn('label=default', source_code)
        # Graphviz might escape newlines differently depending on version
        self.assertTrue('label="in_syslog\n------------\nSyslog Input"' in source_code or 'label="in_syslog\\n------------\\nSyslog Input"' in source_code)
        self.assertTrue('label="out_s3\n------------\nS3 Output"' in source_code or 'label="out_s3\\n------------\\nS3 Output"' in source_code)
        self.assertIn('default_in_syslog -> default_out_s3', source_code)

    def test_generate_graph_no_groups(self):
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {"items": []}

        with self.assertRaises(Exception) as context:
            generate_graph(mock_api_client)

        self.assertTrue("No worker groups found" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
