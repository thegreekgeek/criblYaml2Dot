import unittest
from unittest.mock import MagicMock
from graph_generator import generate_graph

class TestGraphGenerator(unittest.TestCase):
    def test_generate_graph(self):
        api_client = MagicMock()
        api_client.get_worker_groups.return_value = {"items": [{"id": "test_group"}]}
        api_client.get_sources.return_value = {
            "items": [
                {
                    "id": "test_input",
                    "disabled": False,
                    "description": "Test Description",
                    "connections": [{"output": "test_output", "pipeline": "test_pipeline"}],
                }
            ]
        }
        api_client.get_destinations.return_value = {
            "items": [{"id": "test_output", "description": "Test Output Description"}]
        }

        dot = generate_graph(api_client)
        dot_source = str(dot)

        # Check for correct nodes
        self.assertIn("test_group_test_input", dot_source)
        self.assertIn("test_group_test_output", dot_source)

        # Check for correct labels
        self.assertIn("test_input\\n------------\\nTest Description", dot_source)
        self.assertIn("test_output\\n------------\\nTest Output Description", dot_source)

        # Check for correct edge
        self.assertIn("test_group_test_input -> test_group_test_output", dot_source)
        self.assertIn('label=test_pipeline', dot_source)

if __name__ == "__main__":
    unittest.main()
