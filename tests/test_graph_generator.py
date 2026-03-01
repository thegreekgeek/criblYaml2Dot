import unittest
from unittest.mock import MagicMock
from graph_generator import (
    generate_graph,
    _get_node_color,
    _get_edge_attributes,
    _detect_orphan_inputs,
    _detect_orphan_outputs,
    _calculate_pipeline_complexity,
)

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

        # Ensure disabled items are listed in cluster_disabled
        self.assertIn("[D] in_disabled", source_code)
        self.assertNotIn("Disabled Input", source_code)

    def test_generate_graph_missing_metrics(self):
        # Test case where metrics are missing or API fails
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {"items": [{"id": "default"}]}
        mock_api_client.get_sources.return_value = {
            "items": [{"id": "in_syslog", "disabled": False, "connections": [{"output": "out_s3"}]}]
        }
        mock_api_client.get_destinations.return_value = {"items": [{"id": "out_s3"}]}

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
                {"id": "healthy_input", "disabled": False, "connections": [{"output": "out"}]},
                {"id": "unhealthy_input", "disabled": False, "connections": [{"output": "out"}]}
            ]
        }
        mock_api_client.get_destinations.return_value = {
            "items": [
                {"id": "out", "disabled": False}
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
        self.assertEqual(attrs["color"], "gold")
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

    # Feature #2: Configuration Analysis Tests

    def test_detect_orphan_inputs_with_orphans(self):
        """Test detection of inputs with no connections."""
        inputs = [
            {"id": "in_connected", "disabled": False, "connections": [{"output": "out_1"}]},
            {"id": "in_orphan", "disabled": False, "connections": []},
        ]
        connections_map = {
            "in_connected": [{"output": "out_1"}],
            "in_orphan": [],
        }

        orphans = _detect_orphan_inputs(inputs, connections_map)

        self.assertEqual(orphans, {"in_orphan"})
        self.assertNotIn("in_connected", orphans)

    def test_detect_orphan_inputs_all_connected(self):
        """Test when all inputs have connections."""
        inputs = [
            {"id": "in_1", "disabled": False, "connections": [{"output": "out_1"}]},
            {"id": "in_2", "disabled": False, "connections": [{"output": "out_2"}]},
        ]
        connections_map = {
            "in_1": [{"output": "out_1"}],
            "in_2": [{"output": "out_2"}],
        }

        orphans = _detect_orphan_inputs(inputs, connections_map)

        self.assertEqual(orphans, set())

    def test_detect_orphan_inputs_ignores_disabled(self):
        """Test that disabled inputs are not flagged as orphans."""
        inputs = [
            {"id": "in_disabled", "disabled": True, "connections": []},
        ]
        connections_map = {
            "in_disabled": [],
        }

        orphans = _detect_orphan_inputs(inputs, connections_map)

        self.assertEqual(orphans, set())

    def test_detect_orphan_outputs_with_orphans(self):
        """Test detection of outputs with no incoming references."""
        outputs = [
            {"id": "out_used"},
            {"id": "out_orphan"},
        ]
        all_connections = [
            {"output": "out_used", "pipeline": "main"},
        ]

        orphans = _detect_orphan_outputs(outputs, all_connections)

        self.assertEqual(orphans, {"out_orphan"})
        self.assertNotIn("out_used", orphans)

    def test_detect_orphan_outputs_all_referenced(self):
        """Test when all outputs are referenced."""
        outputs = [
            {"id": "out_1"},
            {"id": "out_2"},
        ]
        all_connections = [
            {"output": "out_1", "pipeline": "main"},
            {"output": "out_2", "pipeline": "secondary"},
        ]

        orphans = _detect_orphan_outputs(outputs, all_connections)

        self.assertEqual(orphans, set())

    def test_calculate_pipeline_complexity_low(self):
        """Test complexity scoring for low complexity pipeline."""
        pipeline = {"id": "low", "functions": [{"name": "func1"}, {"name": "func2"}]}

        result = _calculate_pipeline_complexity(pipeline)

        self.assertEqual(result["score"], 2)
        self.assertEqual(result["level"], "low")
        self.assertIn("✓", result["label"])

    def test_calculate_pipeline_complexity_medium(self):
        """Test complexity scoring for medium complexity pipeline."""
        pipeline = {
            "id": "medium",
            "functions": [{"name": f"func{i}"} for i in range(10)],
        }

        result = _calculate_pipeline_complexity(pipeline)

        self.assertEqual(result["score"], 10)
        self.assertEqual(result["level"], "medium")
        self.assertIn("⚠", result["label"])

    def test_calculate_pipeline_complexity_high(self):
        """Test complexity scoring for high complexity pipeline."""
        pipeline = {
            "id": "high",
            "functions": [{"name": f"func{i}"} for i in range(25)],
        }

        result = _calculate_pipeline_complexity(pipeline)

        self.assertEqual(result["score"], 25)
        self.assertEqual(result["level"], "high")
        self.assertIn("🔴", result["label"])

    def test_calculate_pipeline_complexity_no_functions(self):
        """Test complexity scoring when no function data available."""
        pipeline = {"id": "empty"}

        result = _calculate_pipeline_complexity(pipeline)

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["level"], "low")
        self.assertEqual(result["label"], "")

    def test_generate_graph_with_orphan_inputs(self):
        """Test that orphan inputs appear in graph with correct styling."""
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {"items": [{"id": "default"}]}
        mock_api_client.get_sources.return_value = {
            "items": [
                {"id": "in_orphan", "disabled": False, "connections": []},
                {"id": "in_used", "disabled": False, "connections": [{"output": "out_1"}]},
            ]
        }
        mock_api_client.get_destinations.return_value = {"items": [{"id": "out_1"}]}
        mock_api_client.get_source_status.return_value = {"items": []}
        mock_api_client.get_destination_status.return_value = {"items": []}
        mock_api_client.get_source_health.return_value = {"items": []}
        mock_api_client.get_destination_health.return_value = {"items": []}
        mock_api_client.get_pipeline_status.return_value = {"items": []}
        mock_api_client.get_pipelines.return_value = {"items": []}
        mock_api_client.get_pipeline_functions.return_value = {}

        dot = generate_graph(mock_api_client)
        source_code = dot.source

        # Verify orphan input is marked
        self.assertIn("⚠ [ORPHAN] in_orphan", source_code)
        self.assertIn("mistyrose", source_code)  # Light red color

    def test_generate_graph_with_disabled_components(self):
        """Test that disabled items appear in graph with faded styling."""
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {"items": [{"id": "default"}]}
        mock_api_client.get_sources.return_value = {
            "items": [
                {"id": "in_disabled", "disabled": True},
            ]
        }
        mock_api_client.get_destinations.return_value = {"items": []}
        mock_api_client.get_source_status.return_value = {"items": []}
        mock_api_client.get_destination_status.return_value = {"items": []}
        mock_api_client.get_source_health.return_value = {"items": []}
        mock_api_client.get_destination_health.return_value = {"items": []}
        mock_api_client.get_pipeline_status.return_value = {"items": []}
        mock_api_client.get_pipelines.return_value = {"items": []}

        dot = generate_graph(mock_api_client)
        source_code = dot.source

        # Verify disabled input appears with gray styling
        self.assertIn("[D] in_disabled", source_code)
        self.assertIn("lightgray", source_code)
        self.assertIn("dashed", source_code)

    def test_generate_graph_with_complex_pipelines(self):
        """Test that complex pipelines show complexity indicators."""
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {"items": [{"id": "default"}]}
        mock_api_client.get_sources.return_value = {
            "items": [
                {
                    "id": "in_1",
                    "disabled": False,
                    "connections": [{"output": "out_1", "pipeline": "complex"}],
                }
            ]
        }
        mock_api_client.get_destinations.return_value = {"items": [{"id": "out_1"}]}
        mock_api_client.get_source_status.return_value = {"items": []}
        mock_api_client.get_destination_status.return_value = {"items": []}
        mock_api_client.get_source_health.return_value = {"items": []}
        mock_api_client.get_destination_health.return_value = {"items": []}
        mock_api_client.get_pipeline_status.return_value = {"items": []}
        # Return a complex pipeline
        mock_api_client.get_pipelines.return_value = {
            "items": [
                {
                    "id": "complex",
                    "functions": [{"name": f"func{i}"} for i in range(20)],
                }
            ]
        }
        mock_api_client.get_pipeline_functions.return_value = {
            "functions": [{"name": f"func{i}"} for i in range(20)]
        }

        dot = generate_graph(mock_api_client)
        source_code = dot.source

        # Verify complexity indicator appears
        self.assertIn("Complex", source_code)
        self.assertIn("funcs", source_code)

    def test_all_features_work_together(self):
        """Test that Feature #1 and Feature #2 work together."""
        mock_api_client = MagicMock()
        mock_api_client.get_worker_groups.return_value = {"items": [{"id": "default"}]}
        mock_api_client.get_sources.return_value = {
            "items": [
                {
                    "id": "in_syslog",
                    "disabled": False,
                    "connections": [{"output": "out_s3", "pipeline": "main"}],
                },
                {"id": "in_orphan", "disabled": False, "connections": []},
                {"id": "in_disabled", "disabled": True},
            ]
        }
        mock_api_client.get_destinations.return_value = {
            "items": [
                {"id": "out_s3"},
                {"id": "out_orphan"},
            ]
        }
        mock_api_client.get_source_status.return_value = {
            "items": [{"id": "in_syslog", "eps": 100.0}]
        }
        mock_api_client.get_destination_status.return_value = {
            "items": [{"id": "out_s3", "eps": 95.0}]
        }
        mock_api_client.get_source_health.return_value = {
            "items": [{"id": "in_syslog", "error_rate": 2.0}]
        }
        mock_api_client.get_destination_health.return_value = {"items": []}
        mock_api_client.get_pipeline_status.return_value = {"items": []}
        mock_api_client.get_pipelines.return_value = {"items": []}

        # Should not raise any exceptions
        dot = generate_graph(mock_api_client)
        source_code = dot.source

        # Verify all features are present
        self.assertIn("in_syslog", source_code)  # Connected input
        self.assertIn("⚠ [ORPHAN]", source_code)  # Orphan input
        self.assertIn("[D] in_disabled", source_code)  # Disabled input
        self.assertIn("EPS", source_code)  # Feature #1 metrics

if __name__ == '__main__':
    unittest.main()
