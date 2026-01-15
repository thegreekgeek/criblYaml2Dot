import unittest
from unittest.mock import MagicMock
from graph_generator import generate_graph

class TestGraphGenerator(unittest.TestCase):
    def test_generate_graph(self):
        mock_api = MagicMock()
        mock_api.get_worker_groups.return_value = {"items": [{"id": "default"}]}
        mock_api.get_sources.return_value = {
            "items": [
                {
                    "id": "in1",
                    "disabled": False,
                    "connections": [{"output": "out1", "pipeline": "main"}]
                }
            ]
        }
        mock_api.get_destinations.return_value = {"items": [{"id": "out1", "description": "Test Output"}]}

        dot = generate_graph(mock_api)

        # Verify the graph content
        # We can check if certain nodes and edges exist in the dot source
        source = dot.source
        self.assertIn("default", source)
        self.assertIn("in1", source)
        self.assertIn("out1", source)
        self.assertIn("Test Output", source)

if __name__ == "__main__":
    unittest.main()
