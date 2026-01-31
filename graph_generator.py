"""
This module contains logic for generating Graphviz graphs from Cribl configuration.
"""
import graphviz


def generate_graph(api_client):
    """
    Fetches Cribl configurations from the API and returns a graphviz Digraph object.

    Args:
        api_client (CriblAPI): The API client instance to use for fetching configuration.

    Returns:
        graphviz.Digraph: The generated directed graph.

    Raises:
        Exception: If no worker groups are found.
    """
    dot = graphviz.Digraph("Cribl", comment="Cribl Configuration")
    dot.attr(rankdir="LR", splines="polylines", nodesep="0.5", ranksep="1.5")

    groups = api_client.get_worker_groups().get("items", [])
    if not groups:
        raise Exception("No worker groups found.")

    for group in groups:
        group_id = group["id"]

        with dot.subgraph(name=f"cluster_{group_id}") as c:
            c.attr(label=group_id)
            inputs = api_client.get_sources(group_id).get("items", [])
            outputs = api_client.get_destinations(group_id).get("items", [])

            # Create nodes for inputs
            with c.subgraph() as s:
                s.attr(rank="source")
                for input_data in inputs:
                    if not input_data.get("disabled", False):
                        input_id = input_data["id"]
                        description = input_data.get("description", "")
                        label = f"{input_id}"
                        if description:
                            label += f"\n------------\n{description}"
                        s.node(
                            f"{group_id}_{input_id}",
                            label=label,
                            shape="box",
                            style="rounded,filled",
                            fillcolor="lightblue",
                        )

            # Create nodes for outputs
            with c.subgraph() as s:
                s.attr(rank="sink")
                for output_data in outputs:
                    output_id = output_data["id"]
                    description = output_data.get("description", "")
                    label = f"{output_id}"
                    if description:
                        label += f"\n------------\n{description}"
                    s.node(
                        f"{group_id}_{output_id}",
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
                            c.edge(
                                f"{group_id}_{input_id}",
                                f"{group_id}_{output_id}",
                                label=pipeline,
                            )

    return dot
