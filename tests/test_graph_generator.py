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
                },
                {
                    "id": "in_disabled",
                    "description": "Disabled Input",
                    "disabled": True,
                    "connections": []
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

        # Mock status data with EPS
        mock_api_client.get_source_status.return_value = {
            "items": [
                {"id": "in_syslog", "eps": 123.456, "events": 1000}
            ]
        }
        mock_api_client.get_destination_status.return_value = {
            "items": [
                {"id": "out_s3", "eps": 456.789, "events": 5000}
            ]
        }


        # Generate graph
        dot = generate_graph(mock_api_client)

        # Basic assertions on the generated graph content
        source_code = dot.source
        self.assertIn('label=default', source_code)

        # Verify input node label has EPS
        # Check for variations of newline escaping and quoting
        # Graphviz might quote labels if they contain newlines or special chars
        self.assertTrue('label="in_syslog\\n(123.46 EPS)\\n------------\\nSyslog Input"' in source_code or
                        'label="in_syslog\n(123.46 EPS)\n------------\nSyslog Input"' in source_code)

        # Verify output node label has EPS
        self.assertTrue('label="out_s3\\n(456.79 EPS)\\n------------\\nS3 Output"' in source_code or
                        'label="out_s3\n(456.79 EPS)\n------------\nS3 Output"' in source_code)

        self.assertIn('default_in_syslog -> default_out_s3', source_code)

        # Verify disabled inputs are not present
        self.assertNotIn("in_disabled", source_code)
        self.assertNotIn("Disabled Input", source_code)

    def test_generate_graph_missing_metrics(self):
        # Test case where metrics are missing or API fails
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {"items": [{"id": "default"}]}
        mock_api_client.get_sources.return_value = {
            "items": [{"id": "in_syslog", "disabled": False, "connections": []}]
        }
        mock_api_client.get_destinations.return_value = {"items": []}

        # Simulate API failure for status or empty
        mock_api_client.get_source_status.side_effect = Exception("API Error")
        mock_api_client.get_destination_status.return_value = {} # Empty or missing items

        dot = generate_graph(mock_api_client)
        source_code = dot.source

        # Should still generate graph without EPS
        # When description is missing and no EPS, label is just the ID.
        # Graphviz might or might not quote it if it's alphanumeric.
        self.assertTrue('label="in_syslog"' in source_code or 'label=in_syslog' in source_code)
        self.assertNotIn("EPS", source_code)


    def test_generate_graph_no_groups(self):
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {"items": []}

        with self.assertRaises(Exception) as context:
            generate_graph(mock_api_client)

        self.assertIn("No worker groups found", str(context.exception))

if __name__ == '__main__':
    unittest.main()
