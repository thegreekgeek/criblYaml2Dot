# Code Reference

This document provides detailed technical documentation for the Cribl Pipeline Visualizer codebase.

## Table of Contents

- [Environment Variables](#environment-variables)
- [CriblAPI](#criblapi)
- [Graph Generator](#graph-generator)
- [Application (`app.py`)](#application-apppy)

## Environment Variables

The application relies on the following environment variables for configuration. These can be set in a `.env` file or directly in the shell environment.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `CRIBL_BASE_URL` | The base URL of the Cribl Stream API. | `http://localhost:9000` |
| `CRIBL_AUTH_TOKEN` | Authentication token for the Cribl API. If provided, it takes precedence over username/password. | `None` |
| `CRIBL_USERNAME` | Username for Cribl API authentication. Used if `CRIBL_AUTH_TOKEN` is not set. | `None` |
| `CRIBL_PASSWORD` | Password for Cribl API authentication. Used if `CRIBL_AUTH_TOKEN` is not set. | `None` |
| `FLASK_DEBUG` | Enables Flask debug mode if set to `true`. | `False` |

## CriblAPI

The `CriblAPI` class, defined in `cribl_api.py`, handles all interactions with the Cribl Stream API. It manages authentication and provides methods to retrieve configuration data.

### Initialization

```python
CriblAPI(base_url="http://localhost:9000", username=None, password=None, token=None)
```

-   **`base_url`**: The URL of the Cribl Stream instance.
-   **`username`**, **`password`**: Credentials for authentication.
-   **`token`**: An existing bearer token.

The constructor initializes a `requests.Session` object to persist headers (like `Content-Type` and `Authorization`) across requests.
- If a `token` is provided, it is set in the `Authorization` header (prepended with `Bearer ` if missing).
- If `username` and `password` are provided, the `login()` method is called immediately.

### Methods

#### `login(username, password)`
Authenticates with the Cribl API using the provided credentials via `/api/v1/auth/login`. It retrieves the token from the response and updates the session's `Authorization` header.

#### `get_worker_groups()`
Retrieves all worker groups from the API endpoint `/api/v1/master/groups`.

#### `get_sources(group_id)`
Retrieves all input sources for a specific worker group (`group_id`). It queries `/api/v1/m/{group_id}/system/inputs`.

#### `get_destinations(group_id)`
Retrieves all output destinations for a specific worker group (`group_id`). It queries `/api/v1/m/{group_id}/system/outputs`.

#### `get_pipelines(group_id)`
Retrieves all pipelines for a specific worker group (`group_id`). It queries `/api/v1/m/{group_id}/pipelines`.

### Internal Helpers

#### `_get(endpoint)` & `_post(endpoint, payload)`
These internal methods wrap `requests.Session.get` and `requests.Session.post`. They include:
-   **Error Handling**: Catches `requests.exceptions.HTTPError` and `requests.exceptions.RequestException`.
-   **401 Unauthorized**: Specifically catches 401 errors to print a diagnostic message suggesting credential checks.
-   **JSON Decoding**: Decodes the JSON response, handling decode errors gracefully.
-   **Raise for Status**: Calls `response.raise_for_status()` to raise exceptions for HTTP error codes.

### Factory Functions

#### `get_api_client_from_env()`
Reads environment variables (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, `CRIBL_USERNAME`, `CRIBL_PASSWORD`) and instantiates a new `CriblAPI` client.

#### `get_cached_api_client()`
Maintains a global singleton instance (`_cached_api_client`) of the `CriblAPI` client. It calls `get_api_client_from_env()` only if the client hasn't been initialized yet. This ensures the application reuses the same authenticated session.

## Graph Generator

The graph generation logic resides in `graph_generator.py`.

### `generate_graph(api_client)`

This function orchestrates the creation of the Graphviz visualization.

**Parameters:**
-   `api_client`: An instance of `CriblAPI`.

**Process:**
1.  **Initialize Graph**: Creates a `graphviz.Digraph` object with specific attributes (`rankdir="LR"`, `splines="polylines"`).
2.  **Fetch Worker Groups**: Calls `api_client.get_worker_groups()`. If no groups are found, it raises an exception.
3.  **Iterate Groups**: For each worker group, it creates a subgraph (cluster).
4.  **Fetch Configuration**: Retrieves inputs (`get_sources`) and outputs (`get_destinations`) for the group.
5.  **Create Nodes**:
    -   **Inputs**: Iterates through inputs. Skips any input where `disabled` is `True`.
        -   **Style**: `shape="box"`, `style="rounded,filled"`, `fillcolor="lightblue"`.
        -   **Label**: ID + Description (if present).
    -   **Outputs**: Iterates through outputs.
        -   **Style**: `shape="box"`, `style="rounded,filled"`, `fillcolor="lightgreen"`.
        -   **Label**: ID + Description (if present).
6.  **Create Edges**:
    -   Iterates through enabled inputs again.
    -   Checks the `connections` property of each input.
    -   For each connection, if an `output` is specified, it draws an edge from the input ID to the output ID.
    -   The edge is labeled with the pipeline name (defaulting to "passthru").

**Returns:**
-   A `graphviz.Digraph` object representing the pipeline configuration.

## Application (`app.py`)

The `app.py` file is the entry point for the Flask web application.

### Routes

#### `/` (Index)
The main route.
1.  Retrieves the API client via `get_cached_api_client()`.
2.  Calls `generate_graph(api_client)` to build the graph.
3.  Converts the graph to SVG format using `dot.pipe(format="svg")`.
4.  Renders `index.html` with the SVG content embedded.

If an exception occurs (e.g., API connection failure), it catches the exception and renders `error.html` with the error message.

### Execution
When run directly (`__main__`), it starts the Flask development server on `0.0.0.0`. It checks the `FLASK_DEBUG` environment variable to toggle debug mode.
