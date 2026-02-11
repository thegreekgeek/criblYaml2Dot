# Code Reference

This document provides a technical reference for the codebase of the Cribl Pipeline Visualizer.

## Modules

### 1. `app.py`

This is the main entry point for the Flask application.

**Key Components:**

*   **`app`**: The Flask application instance.
*   **`@app.route("/")`**: The main route handler.
    *   Initializes the API client using `get_cached_api_client`.
    *   Calls `generate_graph` to create the visualization.
    *   Renders `index.html` with the SVG content on success.
    *   Renders `error.html` on failure.
*   **`if __name__ == "__main__":`**: Runs the app. Configures debug mode via `FLASK_DEBUG` environment variable.

### 2. `cribl_api.py`

Handles all interactions with the Cribl Stream API.

**Class: `CriblAPI`**

*   **`__init__(self, base_url, username, password, token)`**: Initializes the client.
    *   Sets up a `requests.Session` with JSON headers.
    *   Handles authentication: uses `token` if provided, otherwise attempts to log in with `username` and `password`.
*   **`_post(self, endpoint, payload)`**: Helper method for POST requests. Includes error handling for 401 Unauthorized and JSON decoding errors.
*   **`login(self, username, password)`**: Authenticates with the API using username/password to retrieve a bearer token. Updates the session headers.
*   **`_get(self, endpoint)`**: Helper method for GET requests. Includes similar error handling to `_post`.
*   **`get_worker_groups(self)`**: Fetches all worker groups from `/api/v1/master/groups`.
*   **`get_sources(self, group_id)`**: Fetches inputs for a specific worker group from `/api/v1/m/{group_id}/system/inputs`.
*   **`get_destinations(self, group_id)`**: Fetches outputs for a specific worker group from `/api/v1/m/{group_id}/system/outputs`.
*   **`get_pipelines(self, group_id)`**: Fetches pipelines for a specific worker group from `/api/v1/m/{group_id}/pipelines`.

**Helper Functions:**

*   **`get_api_client_from_env()`**: Creates a `CriblAPI` instance using environment variables (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, `CRIBL_USERNAME`, `CRIBL_PASSWORD`).
*   **`get_cached_api_client()`**: Returns a singleton instance of the API client to reuse the session and token.

### 3. `graph_generator.py`

Responsible for transforming Cribl configuration data into a visual graph.

**Function: `generate_graph(api_client)`**

*   **Arguments**: `api_client` (instance of `CriblAPI`).
*   **Returns**: A `graphviz.Digraph` object.
*   **Logic**:
    1.  Initializes a Digraph with Left-to-Right rank direction (`rankdir="LR"`).
    2.  Fetches worker groups.
    3.  Iterates through each group to create a subgraph (cluster).
    4.  Fetches inputs and outputs for the group.
    5.  **Nodes**: Creates nodes for inputs (rank=source) and outputs (rank=sink).
        *   Filters out disabled inputs.
        *   Uses `id` as the label, appended with `description` if available.
        *   Styles inputs as light blue boxes and outputs as light green boxes.
    6.  **Edges**: Iterates through inputs to find connections.
        *   Draws edges from input to output based on the `connections` list.
        *   Labels the edge with the pipeline name (defaults to "passthru").
