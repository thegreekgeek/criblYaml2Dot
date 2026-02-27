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
-   **`token`**: An optional existing bearer token.

The constructor initializes a `requests.Session` object to persist headers (like `Content-Type` and `Authorization`) across requests. If a token is provided, it is used immediately. If username/password are provided but no token, the `login` method is called.

### Methods

#### `login(username, password)`
Authenticates with the Cribl API using the provided credentials. It updates the session's `Authorization` header with the retrieved token.

#### `get_worker_groups()`
Retrieves all worker groups from the API endpoint `/api/v1/master/groups`.

#### `get_sources(group_id)`
Retrieves all input sources for a specific worker group (`group_id`). It queries `/api/v1/m/{group_id}/system/inputs`.

#### `get_destinations(group_id)`
Retrieves all output destinations for a specific worker group (`group_id`). It queries `/api/v1/m/{group_id}/system/outputs`.

#### `get_pipelines(group_id)`
Retrieves all pipelines for a specific worker group (`group_id`). It queries `/api/v1/m/{group_id}/pipelines`.

#### `get_source_status(group_id)`
Retrieves real-time status metrics for all input sources. It queries `/api/v1/m/{group_id}/system/status/inputs`.
Returns metrics such as EPS (events per second) and event counts.

#### `get_destination_status(group_id)`
Retrieves real-time status metrics for all output destinations. It queries `/api/v1/m/{group_id}/system/status/outputs`.
Returns metrics such as EPS and event counts.

#### `get_pipeline_status(group_id)` *(New - Feature #1)*
Retrieves real-time status metrics for all pipelines. It queries `/api/v1/m/{group_id}/system/status/pipelines`.
Returns pipeline-level metrics including throughput (EPS). Gracefully handles missing endpoint by returning empty items.

#### `get_source_health(group_id)` *(New - Feature #1)*
Retrieves health information for all input sources. It queries `/api/v1/m/{group_id}/system/health/inputs`.
Returns error rates, drop rates, and other health diagnostics. Gracefully handles missing endpoint.

#### `get_destination_health(group_id)` *(New - Feature #1)*
Retrieves health information for all output destinations. It queries `/api/v1/m/{group_id}/system/health/outputs`.
Returns error rates, drop rates, and other health diagnostics. Gracefully handles missing endpoint.

### Helper Methods
-   `_get(endpoint)`: Performs a GET request to the specified endpoint, handling common errors like 401 Unauthorized.
-   `_post(endpoint, payload)`: Performs a POST request to the specified endpoint.

## Graph Generator

The graph generation logic resides in `graph_generator.py`.

### Helper Functions

#### `_get_node_color(health_metrics)` *(New - Feature #1)*
Determines node fill color based on health data.

**Parameters:**
-   `health_metrics` (dict): Health information dictionary with `error_rate` and/or `drop_rate`.

**Returns:**
-   Color name (`"lightcoral"`, `"lightyellow"`, or `None`) based on health thresholds.

**Logic:**
-   `error_rate > 10%` or `drop_rate > 10%` → `"lightcoral"` (critical/red)
-   `5% ≤ error_rate ≤ 10%` or `5% ≤ drop_rate ≤ 10%` → `"lightyellow"` (warning/yellow)
-   Otherwise → `None` (use default color)

#### `_get_edge_attributes(eps_value, max_eps)` *(New - Feature #1)*
Calculates edge styling (penwidth and color) based on throughput (EPS).

**Parameters:**
-   `eps_value` (float): Events per second for this connection.
-   `max_eps` (float): Maximum EPS across all connections (for normalization).

**Returns:**
-   Dictionary with `{"penwidth": "X.XX", "color": "color_name"}`.

**Logic:**
-   Normalizes EPS: `normalized = eps_value / max_eps`
-   Scales penwidth: `1 + (normalized * 4)` → range [1, 5]
-   Color mapping:
    -   `normalized > 0.8` → `"darkred"` (high volume)
    -   `0.5 < normalized ≤ 0.8` → `"orange"` (medium-high volume)
    -   `0.2 < normalized ≤ 0.5` → `"gold"` (medium volume)
    -   `normalized ≤ 0.2` → `"gray"` (low volume)

### `generate_graph(api_client)`

This function orchestrates the creation of the Graphviz visualization with metrics overlay.

**Parameters:**
-   `api_client`: An instance of `CriblAPI`.

**Features (Feature #1: Observability & Metrics Overlay):**
1.  **Real-time metrics** - Fetches EPS, event counts, error rates, and drop rates
2.  **Health-based coloring** - Nodes colored red/yellow/green based on error rates
3.  **Edge metrics** - Pipeline EPS displayed on connection edges
4.  **Dynamic edge styling** - Line thickness and color indicate relative throughput

**Process:**
1.  **Initialize Graph**: Creates a `graphviz.Digraph` object with specific attributes (rankdir="LR", splines="polylines").
2.  **Fetch Worker Groups**: Calls `api_client.get_worker_groups()`. If no groups are found, it raises an exception.
3.  **Iterate Groups**: For each worker group, it creates a subgraph (cluster).
4.  **Fetch Data**: Retrieves:
    -   Inputs (`get_sources`) and input status/health metrics
    -   Outputs (`get_destinations`) and output status/health metrics
    -   Pipeline status metrics (`get_pipeline_status`)
5.  **Calculate Normalization**: Finds max EPS across all nodes/pipelines for edge scaling
6.  **Create Nodes**:
    -   **Inputs**: Iterates through inputs. Skips disabled inputs. Colors based on health (`_get_node_color`). Labels include EPS metrics.
    -   **Outputs**: Same as inputs but with different default color (lightgreen).
7.  **Create Edges**:
    -   Iterates through input connections.
    -   Retrieves pipeline metrics for each connection.
    -   Applies dynamic styling using `_get_edge_attributes` based on EPS.
    -   Labels edges with pipeline name and EPS metrics.

**Error Handling:**
-   All metric API calls wrapped in try-catch
-   Returns empty items if endpoint unavailable
-   Graph renders successfully even if metrics unavailable

**Returns:**
-   A `graphviz.Digraph` object representing the pipeline configuration with metrics overlay.

**Example Output (SVG):**
```
Nodes: Color-coded by health status
  ✓ Light blue/green - Healthy (error_rate < 5%)
  ⚠ Light yellow - Warning (5% ≤ error_rate < 10%)
  ✗ Light coral - Critical (error_rate ≥ 10%)

Edges: Sized and colored by throughput
  ━━━━━ Dark red (>80% of max EPS)
  ━━─── Orange (50-80% of max)
  ─── Gold (20-50% of max)
  ── Gray (<20% of max)

Labels: Include real-time EPS metrics
  in_syslog → out_s3 [main\n(100.00 EPS)]
```

## Application (`app.py`)

The `app.py` file is the entry point for the Flask web application.

### Routes

#### `/` (Index)
The main route.
1.  Retrieves a cached API client instance using `get_cached_api_client()`.
2.  Calls `generate_graph(api_client)` to build the graph.
3.  Converts the graph to SVG format using `dot.pipe(format="svg")`.
4.  Renders `index.html` with the SVG content.

If an exception occurs (e.g., API error), it renders `error.html` with the error message.

### Caching

The application uses a simple global variable `_cached_api_client` to cache the `CriblAPI` instance. This prevents re-authentication on every request. The cache is initialized via `get_cached_api_client()`, which reads environment variables and creates a new client if one doesn't exist.
