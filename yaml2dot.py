import os
import sys

# Check for dependencies
try:
    import graphviz
    import requests
except ImportError as e:
    print(f"Missing dependency: {e.name}. Please install it.", file=sys.stderr)
    if e.name == "requests":
        print("Try: pip install requests", file=sys.stderr)
    elif e.name == "graphviz":
        print("Try: pip install graphviz", file=sys.stderr)
        print(
            "You also need to install the Graphviz command-line tools.",
            file=sys.stderr,
        )
        print("See: https://graphviz.org/download/", file=sys.stderr)
    sys.exit(1)

from cribl_api import get_api_client_from_env


def generate_dot_graph(inputs_config, outputs_config):
    """Generates a Graphviz dot graph from Cribl configurations."""
    dot = graphviz.Digraph("Cribl", comment="Cribl Configuration")
    dot.attr(rankdir="LR", splines="polylines", nodesep="0.5", ranksep="1.5")

    inputs = inputs_config.get("items", [])
    outputs = outputs_config.get("items", [])

    with dot.subgraph() as s:
        s.attr(rank="source")
        for input_data in inputs:
            if not input_data.get("disabled", False):
                input_id = input_data["id"]
                description = input_data.get("description", "")
                label = f"{input_id}"
                if description:
                    label += "\\n ------------"
                    label += f"\\n{description}"
                s.node(
                    input_id,
                    label=label,
                    shape="box",
                    style="rounded,filled",
                    fillcolor="lightblue",
                )

    with dot.subgraph() as s:
        s.attr(rank="sink")
        for output_data in outputs:
            output_id = output_data["id"]
            description = output_data.get("description", "")
            label = f"{output_id}"
            if description:
                label += "\\n ------------"
                label += f"\\n{description}"
            s.node(
                output_id,
                label=label,
                shape="box",
                style="rounded,filled",
                fillcolor="lightgreen",
            )

    # Add edges for connections
    for input_data in inputs:
        if not input_data.get("disabled", False):
            input_id = input_data["id"]
            connections = input_data.get("connections", [])
            for conn in connections:
                if conn and "output" in conn:
                    output_id = conn["output"]
                    pipeline = conn.get("pipeline", "passthru")
                    dot.edge(input_id, output_id, label=pipeline)

    return dot


def get_graph_object(group_id=None):
    """
    Fetches Cribl configurations from the API and returns a graphviz Digraph object.
    """
    api_client = get_api_client_from_env()

    if not group_id:
        groups = api_client.get_worker_groups().get("items", [])
        if not groups:
            raise Exception("No worker groups found.")
        # Default to the first group if no group_id is provided
        group_id = groups[0]["id"]
        print(f"No group_id provided, using the first group found: {group_id}")

    inputs_config = api_client.get_sources(group_id)
    outputs_config = api_client.get_destinations(group_id)

    # Generate the dot graph
    dot_graph = generate_dot_graph(inputs_config, outputs_config)
    return dot_graph


def main():
    """Main function for CLI usage."""
    # The group_id can be passed as a command-line argument
    group_id = sys.argv[1] if len(sys.argv) > 1 else None

    try:
        dot_graph = get_graph_object(group_id)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Save and render the graph
    output_filename = "cribl_flow"
    dot_graph.save(output_filename + ".dot")
    try:
        dot_graph.render(output_filename, view=False, format="png")
        print(f"Generated {output_filename}.png and {output_filename}.dot")
    except graphviz.backend.execute.ExecutableNotFound:
        print(
            f"Generated {output_filename}.dot. You can use an online viewer to render it.",
            file=sys.stderr,
        )
        print(
            "Warning: Graphviz executable not found. Could not render PNG.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
