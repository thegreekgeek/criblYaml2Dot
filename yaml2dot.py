import os
import sys

# Check for dependencies
try:
    import graphviz
    import yaml
except ImportError as e:
    print(f"Missing dependency: {e.name}. Please install it.", file=sys.stderr)
    if e.name == "yaml":
        print("Try: pip install PyYAML", file=sys.stderr)
    elif e.name == "graphviz":
        print("Try: pip install graphviz", file=sys.stderr)
        print(
            "You also need to install the Graphviz command-line tools.",
            file=sys.stderr,
        )
        print("See: https://graphviz.org/download/", file=sys.stderr)
    sys.exit(1)


def find_yaml_files(search_paths, filename):
    """Finds all YAML files with a given filename in a list of search paths."""
    found_files = []
    for path in search_paths:
        for root, _, files in os.walk(path):
            if filename in files:
                found_files.append(os.path.join(root, filename))
    return found_files


def parse_yaml_files(files):
    """Parses a list of YAML files and returns a merged dictionary."""
    config = {}
    for file in files:
        try:
            with open(file, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    # Simple merge: last one wins
                    config.update(data)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {file}: {e}", file=sys.stderr)
        except IOError as e:
            print(f"Error reading file {file}: {e}", file=sys.stderr)
    return config


def generate_dot_graph(inputs_config, outputs_config):
    """Generates a Graphviz dot graph from Cribl configurations."""
    dot = graphviz.Digraph("Cribl", comment="Cribl Configuration")
    dot.attr(rankdir="LR", splines="ortho", nodesep="0.5", ranksep="1.5")

    with dot.subgraph() as s:
        s.attr(rank="source")
        for input_id, input_data in inputs_config.get("inputs", {}).items():
            if not input_data.get("disabled", False):
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
        for output_id, output_data in outputs_config.get("outputs", {}).items():
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
    for input_id, input_data in inputs_config.get("inputs", {}).items():
        if not input_data.get("disabled", False):
            connections = input_data.get("connections", [])
            for conn in connections:
                if conn and "output" in conn:
                    output_id = conn["output"]
                    pipeline = conn.get("pipeline", "passthru")
                    dot.edge(input_id, output_id, label=pipeline)

    return dot


def main():
    """Main function."""
    # Check for dependencies
    try:
        import graphviz
        import yaml
    except ImportError as e:
        print(f"Missing dependency: {e.name}. Please install it.", file=sys.stderr)
        if e.name == "yaml":
            print("Try: pip install PyYAML", file=sys.stderr)
        elif e.name == "graphviz":
            print("Try: pip install graphviz", file=sys.stderr)
            print(
                "You also need to install the Graphviz command-line tools.",
                file=sys.stderr,
            )
            print("See: https://graphviz.org/download/", file=sys.stderr)
        sys.exit(1)

    search_paths = ["default", "local"]

    # Find and parse inputs.yml files
    input_files = find_yaml_files(search_paths, "inputs.yml")
    # a proper implementation would do a deep merge of the configs
    # for now we'll just use the last one found, which is usually the local one
    inputs_config = parse_yaml_files(input_files)

    # Find and parse outputs.yml files
    output_files = find_yaml_files(search_paths, "outputs.yml")
    outputs_config = parse_yaml_files(output_files)

    # Generate the dot graph
    dot_graph = generate_dot_graph(inputs_config, outputs_config)

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
