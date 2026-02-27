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


def _detect_orphan_inputs(inputs, connections_map):
    """
    Identifies input sources that have no outgoing connections.
    An orphan input is one that is not routed to any output.

    Args:
        inputs (list): List of input source objects.
        connections_map (dict): Dict mapping input_id → list of output connections.

    Returns:
        set: IDs of orphaned input sources.
    """
    orphan_inputs = set()

    for input_data in inputs:
        if not input_data.get("disabled", False):
            input_id = input_data["id"]
            connections = connections_map.get(input_id, [])

            # If no connections, it's an orphan
            if not connections or len(connections) == 0:
                orphan_inputs.add(input_id)

    return orphan_inputs


def _detect_orphan_outputs(outputs, all_connections):
    """
    Identifies output destinations with no incoming connections.
    An orphan output is one that is not referenced by any input.

    Args:
        outputs (list): List of output destination objects.
        all_connections (list): All connection objects from all inputs.

    Returns:
        set: IDs of orphaned output destinations.
    """
    # Collect all output IDs that are referenced in connections
    referenced_outputs = set()

    for conn in all_connections:
        if conn and "output" in conn:
            referenced_outputs.add(conn["output"])

    # Find outputs not in the referenced set
    orphan_outputs = set()
    for output_data in outputs:
        output_id = output_data["id"]
        if output_id not in referenced_outputs:
            orphan_outputs.add(output_id)

    return orphan_outputs


def _calculate_pipeline_complexity(pipeline_obj):
    """
    Calculates complexity score for a pipeline based on function count.
    Higher function count = higher complexity.

    Args:
        pipeline_obj (dict): Pipeline object with 'functions' or 'config' field.

    Returns:
        dict: {
            "score": int,           # Number of functions
            "level": str,           # "low", "medium", or "high"
            "label": str           # Display label with indicator
        }

    Thresholds:
        - score < 5:   "low"      (efficient)
        - score 5-15:  "medium"   (complex, watch)
        - score > 15:  "high"     (very complex, refactor)
    """
    # Try to get function count from pipeline object
    function_count = 0

    # Method 1: Direct functions list
    if "functions" in pipeline_obj and isinstance(pipeline_obj["functions"], list):
        function_count = len(pipeline_obj["functions"])
    # Method 2: Direct function_count field
    elif "function_count" in pipeline_obj:
        function_count = int(pipeline_obj.get("function_count", 0))
    # Method 3: Count functions in config if available
    elif "config" in pipeline_obj and isinstance(pipeline_obj["config"], dict):
        config = pipeline_obj["config"]
        if "functions" in config:
            function_count = len(config["functions"])

    # Classify complexity
    if function_count < 5:
        level = "low"
        indicator = "✓"
    elif function_count <= 15:
        level = "medium"
        indicator = "⚠"
    else:
        level = "high"
        indicator = "🔴"

    return {
        "score": function_count,
        "level": level,
        "label": f"{indicator} ({function_count} funcs)" if function_count > 0 else ""
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

            # Feature #2: Configuration Analysis
            # Build a map of connections by input ID
            connections_map = {}
            all_connections = []
            for input_data in inputs:
                input_id = input_data["id"]
                connections = input_data.get("connections", [])
                connections_map[input_id] = connections
                all_connections.extend(connections)

            # Detect orphan inputs and outputs
            try:
                orphan_inputs = _detect_orphan_inputs(inputs, connections_map)
            except Exception as e:
                print(f"Failed to detect orphan inputs for group {group_id}: {e}")
                orphan_inputs = set()

            try:
                orphan_outputs = _detect_orphan_outputs(outputs, all_connections)
            except Exception as e:
                print(f"Failed to detect orphan outputs for group {group_id}: {e}")
                orphan_outputs = set()

            # Get pipeline functions for complexity scoring
            try:
                pipelines = api_client.get_pipelines(group_id).get("items", [])
                pipeline_complexity = {}
                for pipeline in pipelines:
                    pipeline_id = pipeline["id"]
                    # Try to get detailed function info
                    try:
                        pipeline_detail = api_client.get_pipeline_functions(group_id, pipeline_id)
                        complexity = _calculate_pipeline_complexity(pipeline_detail)
                    except Exception:
                        # If detailed fetch fails, use basic info
                        complexity = _calculate_pipeline_complexity(pipeline)
                    pipeline_complexity[pipeline_id] = complexity
            except Exception as e:
                print(f"Failed to calculate pipeline complexity for group {group_id}: {e}")
                pipeline_complexity = {}

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
                    input_id = input_data["id"]
                    is_disabled = input_data.get("disabled", False)
                    is_orphan = input_id in orphan_inputs

                    # Skip creating node for disabled items in main loop (we'll handle below)
                    if is_disabled:
                        continue

                    description = input_data.get("description", "")
                    label = f"{input_id}"

                    # Add orphan indicator if applicable
                    if is_orphan:
                        label = f"⚠ [ORPHAN] {label}"

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

                    # Determine node color based on Feature #2 analysis priority
                    if is_orphan:
                        # Orphan nodes get red styling
                        fillcolor = "mistyrose"  # Light red
                        border_style = "rounded,filled,bold"
                        border_color = "red"
                    else:
                        # Use Feature #1 health-based color
                        health = source_health_map.get(input_id)
                        fillcolor = _get_node_color(health) or "lightblue"
                        border_style = "rounded,filled"
                        border_color = None

                    node_kwargs = {
                        "label": label,
                        "shape": "box",
                        "style": border_style,
                        "fillcolor": fillcolor,
                    }
                    if border_color:
                        node_kwargs["color"] = border_color

                    s.node(f"{group_id}_{input_id}", **node_kwargs)

                # Now render disabled inputs with faded styling
                for input_data in inputs:
                    if input_data.get("disabled", False):
                        input_id = input_data["id"]
                        description = input_data.get("description", "")
                        label = f"[DISABLED] {input_id}"

                        if description:
                            label += f"\n------------\n{description}"

                        s.node(
                            f"{group_id}_{input_id}",
                            label=label,
                            shape="box",
                            style="rounded,filled,dashed",
                            fillcolor="lightgray",
                            color="gray",
                            penwidth="0.6",
                        )

            # Create nodes for outputs
            with c.subgraph() as s:
                s.attr(rank="sink")
                for output_data in outputs:
                    output_id = output_data["id"]
                    is_disabled = output_data.get("disabled", False)
                    is_orphan = output_id in orphan_outputs

                    # Skip creating node for disabled items in main loop
                    if is_disabled:
                        continue

                    description = output_data.get("description", "")
                    label = f"{output_id}"

                    # Add orphan indicator if applicable
                    if is_orphan:
                        label = f"⚠ [ORPHAN] {label}"

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

                    # Determine node color based on Feature #2 analysis priority
                    if is_orphan:
                        # Orphan nodes get red styling
                        fillcolor = "mistyrose"  # Light red
                        border_style = "rounded,filled,bold"
                        border_color = "red"
                    else:
                        # Use Feature #1 health-based color
                        health = dest_health_map.get(output_id)
                        fillcolor = _get_node_color(health) or "lightgreen"
                        border_style = "rounded,filled"
                        border_color = None

                    node_kwargs = {
                        "label": label,
                        "shape": "box",
                        "style": border_style,
                        "fillcolor": fillcolor,
                    }
                    if border_color:
                        node_kwargs["color"] = border_color

                    s.node(f"{group_id}_{output_id}", **node_kwargs)

                # Now render disabled outputs with faded styling
                for output_data in outputs:
                    if output_data.get("disabled", False):
                        output_id = output_data["id"]
                        description = output_data.get("description", "")
                        label = f"[DISABLED] {output_id}"

                        if description:
                            label += f"\n------------\n{description}"

                        s.node(
                            f"{group_id}_{output_id}",
                            label=label,
                            shape="box",
                            style="rounded,filled,dashed",
                            fillcolor="lightgray",
                            color="gray",
                            penwidth="0.6",
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

                            # Feature #2: Add complexity information to edge label
                            complexity = pipeline_complexity.get(pipeline, {})
                            if complexity.get("label"):
                                complexity_label = complexity["label"]
                                # Add complexity indicator to edge
                                if complexity["level"] == "high":
                                    edge_label += f"\n⚠ Complex {complexity_label}"
                                elif complexity["level"] == "medium":
                                    edge_label += f"\n{complexity_label}"

                            # Get edge styling based on throughput (Feature #1)
                            edge_attrs = _get_edge_attributes(edge_eps, max_eps)

                            c.edge(
                                f"{group_id}_{input_id}",
                                f"{group_id}_{output_id}",
                                label=edge_label,
                                penwidth=edge_attrs["penwidth"],
                                color=edge_attrs["color"],
                            )

    return dot
