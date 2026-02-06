# Code Reference

This document provides a reference for the codebase of the Cribl Pipeline Visualizer.

## Core Modules

### `app.py`

The main entry point for the Flask application.

*   **`index()`**: The main route (`/`) that handles:
    *   Initializing/retrieving the cached `CriblAPI` client.
    *   Calling `generate_graph` to create the pipeline visualization.
    *   Rendering `index.html` with the generated SVG or `error.html` on failure.

### `cribl_api.py`

Handles interactions with the Cribl Stream API.

#### `CriblAPI` Class

A client for making authenticated requests to Cribl Stream.

*   **`__init__(base_url, username, password, token)`**: Initializes the client.
    *   `base_url`: Defaults to `http://localhost:9000`.
    *   `token`: Takes precedence if provided.
    *   `username`/`password`: Used to log in if token is missing.

*   **`login(username, password)`**: Authenticates against `/api/v1/auth/login` and sets the `Authorization` header.

*   **`get_worker_groups()`**: Fetches all worker groups from `/api/v1/master/groups`.

*   **`get_sources(group_id)`**: Fetches inputs for a specific group from `/api/v1/m/{group_id}/system/inputs`.

*   **`get_destinations(group_id)`**: Fetches outputs for a specific group from `/api/v1/m/{group_id}/system/outputs`.

*   **`get_pipelines(group_id)`**: Fetches pipelines for a specific group from `/api/v1/m/{group_id}/pipelines`.

#### Helper Functions

*   **`get_cached_api_client()`**: Returns a singleton-like instance of `CriblAPI` initialized from environment variables (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, etc.).

### `graph_generator.py`

Logic for transforming Cribl configuration data into a visual graph.

*   **`generate_graph(api_client)`**:
    1.  Fetches worker groups.
    2.  For each group, creates a cluster.
    3.  Fetches inputs (sources) and outputs (destinations).
    4.  Creates graph nodes for non-disabled inputs and outputs.
    5.  Draws edges based on input connections (routing through pipelines).
    6.  Returns a `graphviz.Digraph` object.

## Data Flow

1.  **Request**: User accesses the web interface.
2.  **API Call**: `app.py` requests data via `CriblAPI`.
3.  **Processing**: `graph_generator.py` processes the JSON response and builds a graph structure.
4.  **Rendering**: `graphviz` renders the graph to SVG format.
5.  **Response**: The SVG is embedded in the HTML response.
