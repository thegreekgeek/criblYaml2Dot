# Code Reference

This document provides a technical overview of the Cribl Pipeline Visualizer codebase, detailing the architecture, modules, and key components.

## Architecture

The application is built using the Flask web framework. It follows a simple architecture:
1.  **Web Request**: A user accesses the root URL (`/`).
2.  **API Client**: The application uses a cached `CriblAPI` client to connect to the configured Cribl Stream instance.
3.  **Data Fetching**: The client retrieves worker groups, inputs, outputs, and pipeline configurations.
4.  **Graph Generation**: The `graph_generator` module processes this data and constructs a Graphviz `Digraph` object.
5.  **Rendering**: The graph is rendered as an SVG and embedded in the HTML response.

## Modules

### `app.py`

The main entry point for the Flask application.

*   **`index()`**: The primary route handler for `/`. It:
    *   Retrieves the cached `CriblAPI` client.
    *   Calls `generate_graph` to create the visualization.
    *   Renders the `index.html` template with the SVG content.
    *   Handles exceptions by rendering `error.html` with the error message.

### `cribl_api.py`

Handles all interactions with the Cribl Stream API.

*   **`CriblAPI` Class**:
    *   **`__init__(base_url, username, password, token)`**: Initializes the API client. It sets up a `requests.Session` for connection pooling. If a token is provided, it is used directly; otherwise, it attempts to log in with the username and password.
    *   **`login(username, password)`**: Authenticates with the Cribl API and retrieves a JWT token. The token is stored in the session headers for subsequent requests.
    *   **`get_worker_groups()`**: Fetches the list of worker groups from `/api/v1/master/groups`.
    *   **`get_sources(group_id)`**: Fetches input configurations for a specific worker group.
    *   **`get_destinations(group_id)`**: Fetches output configurations for a specific worker group.
    *   **`get_pipelines(group_id)`**: Fetches pipeline configurations for a specific worker group.

*   **`get_cached_api_client()`**: A helper function that implements a singleton pattern to reuse the API client instance across requests, preventing redundant logins.

### `graph_generator.py`

Contains the logic for transforming Cribl configuration data into a visual graph.

*   **`generate_graph(api_client)`**: The core function.
    *   **Input**: An instance of `CriblAPI`.
    *   **Output**: A `graphviz.Digraph` object.
    *   **Logic**:
        *   Iterates through each worker group.
        *   Creates a subgraph (cluster) for each group.
        *   **Inputs**: Adds nodes for inputs, filtering out any that have `disabled=True`.
        *   **Outputs**: Adds nodes for outputs.
        *   **Connections**: Iterates through inputs and adds edges to their connected outputs based on the configured pipeline.
        *   **Attributes**: Sets graph attributes like `rankdir="LR"` (Left-to-Right layout) and node styles.

## Templates

The application uses Jinja2 templates located in the `templates/` directory:

*   **`index.html`**: Displays the generated SVG graph. It accepts `svg_content` as a variable.
*   **`error.html`**: Displays an error message if graph generation fails. It accepts `error_message` as a variable.

## Environment Variables

The application relies on the following environment variables (loaded via `python-dotenv`):

*   `CRIBL_BASE_URL`: The URL of the Cribl Stream instance (default: `http://localhost:9000`).
*   `CRIBL_AUTH_TOKEN`: A valid authentication token.
*   `CRIBL_USERNAME` / `CRIBL_PASSWORD`: Credentials used for authentication if `CRIBL_AUTH_TOKEN` is not provided.
*   `FLASK_DEBUG`: specific Flask debug mode (default: `False`).
