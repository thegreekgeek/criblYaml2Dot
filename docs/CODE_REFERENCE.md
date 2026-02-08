# Code Reference

This document provides a detailed reference for the core components of the Cribl Pipeline Visualizer.

## `app.py`

The main entry point for the Flask application. It defines the web routes and orchestrates the data fetching and graph generation.

### Global Variables

*   **`app`**: The Flask application instance.
*   **`debug_mode`**: Boolean flag read from the `FLASK_DEBUG` environment variable (default: `False`).

### Routes

#### `GET /`

The index route. It performs the following actions:
1.  Retrieves a cached `CriblAPI` client using `get_cached_api_client()`.
2.  Calls `generate_graph(api_client)` to fetch data and build the Graphviz object.
3.  Renders the graph to SVG format.
4.  Returns the `index.html` template with the SVG content.

**Error Handling:**
*   Catches generic `Exception` during the graph generation process.
*   Renders `error.html` with the error message if an exception occurs (e.g., API connection failure).

## `cribl_api.py`

Handles all interactions with the Cribl Stream API.

### `CriblAPI` Class

A client for interacting with the Cribl API.

#### `__init__(self, base_url="http://localhost:9000", username=None, password=None, token=None)`

Initializes the client.
*   Sets up a `requests.Session`.
*   Authenticates using a token (if provided) or username/password.
*   Sets the `Authorization` header for subsequent requests.

#### `login(self, username, password)`

Authenticates with the Cribl API using username and password to retrieve a Bearer token.
*   POSTs to `/api/v1/auth/login`.
*   Updates the session's `Authorization` header.

#### `get_worker_groups(self)`

Retrieves all worker groups from the master node.
*   **Endpoint:** `/api/v1/master/groups`
*   **Returns:** JSON response containing the list of worker groups.

#### `get_sources(self, group_id)`

Retrieves all sources (inputs) for a specific worker group.
*   **Endpoint:** `/api/v1/m/{group_id}/system/inputs`
*   **Args:** `group_id` (str) - The ID of the worker group.
*   **Returns:** JSON response containing the list of sources.

#### `get_destinations(self, group_id)`

Retrieves all destinations (outputs) for a specific worker group.
*   **Endpoint:** `/api/v1/m/{group_id}/system/outputs`
*   **Args:** `group_id` (str) - The ID of the worker group.
*   **Returns:** JSON response containing the list of destinations.

#### `get_pipelines(self, group_id)`

Retrieves all pipelines for a specific worker group.
*   **Endpoint:** `/api/v1/m/{group_id}/pipelines`
*   **Args:** `group_id` (str) - The ID of the worker group.
*   **Returns:** JSON response containing the list of pipelines.

### Helper Functions

#### `get_api_client_from_env()`

Factory function that creates a `CriblAPI` instance using environment variables:
*   `CRIBL_BASE_URL`
*   `CRIBL_AUTH_TOKEN`
*   `CRIBL_USERNAME`
*   `CRIBL_PASSWORD`

#### `get_cached_api_client()`

Returns a singleton instance of the `CriblAPI` client. It initializes the client on the first call using `get_api_client_from_env()` and caches it for subsequent calls.

## `graph_generator.py`

Contains the logic for transforming Cribl configuration data into a visual graph.

### `generate_graph(api_client)`

Fetches configuration from the API and builds a Graphviz `Digraph`.

*   **Args:** `api_client` (`CriblAPI`) - An authenticated API client instance.
*   **Returns:** `graphviz.Digraph` - The generated graph object.
*   **Raises:** `Exception` if no worker groups are found.

**Logic:**
1.  Creates a main `Digraph` with left-to-right rank direction.
2.  Iterates through each worker group fetched from the API.
3.  Creates a subgraph (cluster) for each worker group.
4.  Fetches inputs and outputs for the group.
5.  **Inputs:** Creates nodes for enabled inputs (rank=`source`), styled as blue boxes.
6.  **Outputs:** Creates nodes for outputs (rank=`sink`), styled as green boxes.
7.  **Edges:** Iterates through inputs and their connections. Adds edges from input to output, labeled with the pipeline name (or "passthru").
