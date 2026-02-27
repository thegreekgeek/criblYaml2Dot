import unittest
from unittest.mock import MagicMock
from graph_generator import generate_graph, _get_node_color, _get_edge_attributes

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

        # Mock health data
        mock_api_client.get_source_health.return_value = {"items": []}
        mock_api_client.get_destination_health.return_value = {"items": []}
        mock_api_client.get_pipeline_status.return_value = {"items": []}

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
        mock_api_client.get_destination_status.return_value = {"items": []}
        mock_api_client.get_source_health.return_value = {"items": []}
        mock_api_client.get_destination_health.return_value = {"items": []}
        mock_api_client.get_pipeline_status.return_value = {"items": []}

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

    def test_generate_graph_with_health_status(self):
        """Test that health status affects node coloring."""
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {
            "items": [{"id": "default"}]
        }
        mock_api_client.get_sources.return_value = {
            "items": [
                {"id": "healthy_input", "disabled": False, "connections": []},
                {"id": "unhealthy_input", "disabled": False, "connections": []}
            ]
        }
        mock_api_client.get_destinations.return_value = {"items": []}

        # Status data
        mock_api_client.get_source_status.return_value = {"items": []}
        mock_api_client.get_destination_status.return_value = {"items": []}

        # Health data - unhealthy_input has high error rate
        mock_api_client.get_source_health.return_value = {
            "items": [
                {"id": "healthy_input", "error_rate": 0.5},
                {"id": "unhealthy_input", "error_rate": 15.0}  # > 10% = critical
            ]
        }
        mock_api_client.get_destination_health.return_value = {"items": []}
        mock_api_client.get_pipeline_status.return_value = {"items": []}

        dot = generate_graph(mock_api_client)
        source_code = dot.source

        # Verify that unhealthy input gets red color
        self.assertIn('fillcolor=lightcoral', source_code)
        # Healthy input should use default color
        self.assertIn('fillcolor=lightblue', source_code)

    def test_generate_graph_with_edge_metrics(self):
        """Test that edge metrics are included in the graph."""
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {
            "items": [{"id": "default"}]
        }
        mock_api_client.get_sources.return_value = {
            "items": [
                {
                    "id": "in_1",
                    "disabled": False,
                    "connections": [{"output": "out_1", "pipeline": "main"}]
                }
            ]
        }
        mock_api_client.get_destinations.return_value = {
            "items": [{"id": "out_1", "disabled": False}]
        }

        # Status data
        mock_api_client.get_source_status.return_value = {"items": []}
        mock_api_client.get_destination_status.return_value = {"items": []}

        # Pipeline metrics - main pipeline has 100 EPS
        mock_api_client.get_pipeline_status.return_value = {
            "items": [{"id": "main", "eps": 100.0}]
        }

        # Health data
        mock_api_client.get_source_health.return_value = {"items": []}
        mock_api_client.get_destination_health.return_value = {"items": []}

        dot = generate_graph(mock_api_client)
        source_code = dot.source

        # Verify edge has EPS metric in label
        self.assertIn('(100.00 EPS)', source_code)
        # Verify edge has color attribute
        self.assertIn('color=', source_code)
        # Verify edge has penwidth attribute
        self.assertIn('penwidth=', source_code)

    def test_get_node_color_healthy(self):
        """Test color calculation for healthy node."""
        health = {"error_rate": 2.0, "drop_rate": 1.0}
        color = _get_node_color(health)
        self.assertIsNone(color)  # None means use default

    def test_get_node_color_warning(self):
        """Test color calculation for warning state."""
        health = {"error_rate": 7.0}  # Between 5 and 10
        color = _get_node_color(health)
        self.assertEqual(color, "lightyellow")

    def test_get_node_color_critical(self):
        """Test color calculation for critical state."""
        health = {"drop_rate": 12.0}  # > 10
        color = _get_node_color(health)
        self.assertEqual(color, "lightcoral")

    def test_get_node_color_none(self):
        """Test color calculation when no health data."""
        color = _get_node_color(None)
        self.assertIsNone(color)

    def test_get_edge_attributes_high_volume(self):
        """Test edge styling for high volume traffic."""
        attrs = _get_edge_attributes(900, 1000)
        self.assertEqual(attrs["color"], "darkred")
        self.assertGreater(float(attrs["penwidth"]), 3.0)

    def test_get_edge_attributes_medium_volume(self):
        """Test edge styling for medium volume traffic."""
        attrs = _get_edge_attributes(500, 1000)
        self.assertEqual(attrs["color"], "orange")
        self.assertGreater(float(attrs["penwidth"]), 2.0)

    def test_get_edge_attributes_low_volume(self):
        """Test edge styling for low volume traffic."""
        attrs = _get_edge_attributes(100, 1000)
        self.assertEqual(attrs["color"], "gray")
        self.assertGreater(float(attrs["penwidth"]), 1.0)

    def test_get_edge_attributes_no_data(self):
        """Test edge styling when no EPS data available."""
        attrs = _get_edge_attributes(None, 1000)
        self.assertEqual(attrs["color"], "gray")
        self.assertEqual(attrs["penwidth"], "1")

if __name__ == '__main__':
    unittest.main()
