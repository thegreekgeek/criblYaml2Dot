import graphviz


def generate_graph(api_client):
    """
    Fetches Cribl configurations from the API and returns a graphviz Digraph object.

    Args:
        api_client (CriblAPI): An instance of the CriblAPI client.

    Returns:
        graphviz.Digraph: The generated graph showing inputs, outputs, and pipeline connections.

    Raises:
        Exception: If no worker groups are found.
    """
    dot = graphviz.Digraph("Cribl", comment="Cribl Configuration")
    dot.attr(rankdir="LR", splines="polyline", nodesep="0.5", ranksep="1.5")

    groups = api_client.get_worker_groups().get("items", [])
    if not groups:
        raise Exception("No worker groups found.")

    for group in groups:
        group_id = group["id"]

        with dot.subgraph(name=f"cluster_{group_id}") as c:
            c.attr(label=group_id)
            inputs = api_client.get_sources(group_id).get("items", [])
            outputs = api_client.get_destinations(group_id).get("items", [])

            # Fetch status for metrics
            try:
                source_status = api_client.get_source_status(group_id).get("items", [])
                source_metrics = {item["id"]: item for item in source_status}
            except Exception as e:
                print(f"Failed to fetch source status for group {group_id}: {e}")
                source_metrics = {}

            try:
                dest_status = api_client.get_destination_status(group_id).get("items", [])
                dest_metrics = {item["id"]: item for item in dest_status}
            except Exception as e:
                print(f"Failed to fetch destination status for group {group_id}: {e}")
                dest_metrics = {}

            # Create nodes for inputs
            with c.subgraph() as s:
                s.attr(rank="source")
                for input_data in inputs:
                    if not input_data.get("disabled", False):
                        input_id = input_data["id"]
                        description = input_data.get("description", "")
                        label = f"{input_id}"

                        # Add EPS metric if available
                        metrics = source_metrics.get(input_id)
                        if metrics:
                            # Try to find EPS or events count
                            eps = metrics.get("eps")
                            if eps is not None:
                                label += f"\n({eps:.2f} EPS)"
                            elif "events" in metrics:
                                label += f"\n({metrics['events']} Events)"

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

                    # Add EPS metric if available
                    metrics = dest_metrics.get(output_id)
                    if metrics:
                         # Try to find EPS or events count
                        eps = metrics.get("eps")
                        if eps is not None:
                            label += f"\n({eps:.2f} EPS)"
                        elif "events" in metrics:
                            label += f"\n({metrics['events']} Events)"

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
