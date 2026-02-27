import graphviz


def _get_node_color(health_metrics):
    """
    Determines node color based on health metrics.

    Args:
        health_metrics (dict): Health information for the node.

    Returns:
        str: Color name for the node (green, yellow, or red).
    """
    if not health_metrics:
        return None

    # Check for error_rate or drop_rate
    error_rate = health_metrics.get("error_rate", 0)
    drop_rate = health_metrics.get("drop_rate", 0)

    # Critical: > 10%
    if error_rate > 10 or drop_rate > 10:
        return "lightcoral"  # Red
    # Warning: > 5%
    elif error_rate > 5 or drop_rate > 5:
        return "lightyellow"  # Yellow
    # Healthy
    else:
        return None  # Use default color


def _get_edge_attributes(eps_value, max_eps):
    """
    Determines edge styling based on EPS (events per second).

    Args:
        eps_value (float): Events per second for this connection.
        max_eps (float): Maximum EPS across all connections (for scaling).

    Returns:
        dict: Dictionary with 'penwidth' and 'color' attributes.
    """
    if not eps_value or max_eps == 0:
        return {"penwidth": "1", "color": "gray"}

    # Scale penwidth from 1 to 5
    normalized_eps = min(eps_value / max_eps, 1.0)
    penwidth = 1 + (normalized_eps * 4)

    # Color based on relative volume
    if normalized_eps > 0.8:
        color = "darkred"  # High volume
    elif normalized_eps > 0.5:
        color = "orange"  # Medium-high volume
    elif normalized_eps > 0.2:
        color = "gold"  # Medium volume
    else:
        color = "gray"  # Low volume

    return {
        "penwidth": str(round(penwidth, 2)),
        "color": color
    }


def generate_graph(api_client):
    """
    Fetches Cribl configurations from the API and returns a graphviz Digraph object.

    Includes metrics overlay showing:
    - EPS (Events Per Second) on nodes and edges
    - Health status via node coloring
    - Edge thickness and color based on throughput volume

    Args:
        api_client (CriblAPI): An instance of the CriblAPI client.

    Returns:
        graphviz.Digraph: The generated graph showing inputs, outputs, and pipeline connections.

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

            # Fetch metrics and health data
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

            try:
                source_health = api_client.get_source_health(group_id).get("items", [])
                source_health_map = {item["id"]: item for item in source_health}
            except Exception as e:
                print(f"Failed to fetch source health for group {group_id}: {e}")
                source_health_map = {}

            try:
                dest_health = api_client.get_destination_health(group_id).get("items", [])
                dest_health_map = {item["id"]: item for item in dest_health}
            except Exception as e:
                print(f"Failed to fetch destination health for group {group_id}: {e}")
                dest_health_map = {}

            try:
                pipeline_status = api_client.get_pipeline_status(group_id).get("items", [])
                pipeline_metrics = {item["id"]: item for item in pipeline_status}
            except Exception as e:
                print(f"Failed to fetch pipeline status for group {group_id}: {e}")
                pipeline_metrics = {}

            # Calculate max EPS for edge scaling
            all_eps_values = []
            for metrics in source_metrics.values():
                eps = metrics.get("eps")
                if eps is not None:
                    all_eps_values.append(eps)
            for metrics in dest_metrics.values():
                eps = metrics.get("eps")
                if eps is not None:
                    all_eps_values.append(eps)
            max_eps = max(all_eps_values) if all_eps_values else 0

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
                            eps = metrics.get("eps")
                            if eps is not None:
                                label += f"\n({eps:.2f} EPS)"
                            elif "events" in metrics:
                                label += f"\n({metrics['events']} Events)"

                        if description:
                            label += f"\n------------\n{description}"

                        # Determine node color based on health
                        health = source_health_map.get(input_id)
                        fillcolor = _get_node_color(health) or "lightblue"

                        s.node(
                            f"{group_id}_{input_id}",
                            label=label,
                            shape="box",
                            style="rounded,filled",
                            fillcolor=fillcolor,
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
                        eps = metrics.get("eps")
                        if eps is not None:
                            label += f"\n({eps:.2f} EPS)"
                        elif "events" in metrics:
                            label += f"\n({metrics['events']} Events)"

                    if description:
                        label += f"\n------------\n{description}"

                    # Determine node color based on health
                    health = dest_health_map.get(output_id)
                    fillcolor = _get_node_color(health) or "lightgreen"

                    s.node(
                        f"{group_id}_{output_id}",
                        label=label,
                        shape="box",
                        style="rounded,filled",
                        fillcolor=fillcolor,
                    )

            # Add edges for connections with metrics overlay
            for input_data in inputs:
                if not input_data.get("disabled", False):
                    input_id = input_data["id"]
                    connections = input_data.get("connections", [])
                    for conn in connections:
                        if conn and "output" in conn:
                            output_id = conn["output"]
                            pipeline = conn.get("pipeline", "passthru")

                            # Get pipeline metrics for edge labeling
                            pipeline_metrics_data = pipeline_metrics.get(pipeline, {})
                            edge_eps = pipeline_metrics_data.get("eps", 0)
                            edge_label = pipeline

                            if edge_eps > 0:
                                edge_label += f"\n({edge_eps:.2f} EPS)"

                            # Get edge styling based on throughput
                            edge_attrs = _get_edge_attributes(edge_eps, max_eps)

                            c.edge(
                                f"{group_id}_{input_id}",
                                f"{group_id}_{output_id}",
                                label=edge_label,
                                penwidth=edge_attrs["penwidth"],
                                color=edge_attrs["color"],
                            )

    return dot
