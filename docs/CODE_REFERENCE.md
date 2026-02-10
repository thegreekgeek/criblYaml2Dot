# Code Reference

This document provides technical details for the internal modules of the Cribl Pipeline Visualizer.

## `app.py`

The main Flask application entry point.

### Functions

#### `index()`
- **Route**: `/`
- **Method**: `GET`
- **Description**: The main route that generates the graph and renders it.
- **Returns**: Rendered HTML template with the graph SVG (`index.html`) or an error page (`error.html`) if an exception occurs.

### Configuration
- **`FLASK_DEBUG`**: Environment variable to enable Flask debug mode. Defaults to `False`.

## `cribl_api.py`

Client library for interacting with the Cribl API.

### Class: `CriblAPI`

A client for interacting with the Cribl API.

#### `__init__(self, base_url="http://localhost:9000", username=None, password=None, token=None)`
- **Description**: Initializes the CriblAPI client.
- **Args**:
    - `base_url` (str): The base URL of the Cribl API.
    - `username` (str, optional): The username for authentication.
    - `password` (str, optional): The password for authentication.
    - `token` (str, optional): An existing authentication token.

#### `login(self, username, password)`
- **Description**: Logs in to the Cribl API and retrieves an authentication token.
- **Args**:
    - `username` (str): The username.
    - `password` (str): The password.

#### `get_worker_groups(self)`
- **Description**: Retrieves all worker groups.
- **Endpoint**: `/api/v1/master/groups`
- **Returns**: JSON response containing worker groups.

#### `get_sources(self, group_id)`
- **Description**: Retrieves all sources (inputs) for a given worker group.
- **Endpoint**: `/api/v1/m/{group_id}/system/inputs`
- **Args**:
    - `group_id` (str): The ID of the worker group.
- **Returns**: JSON response containing sources.

#### `get_destinations(self, group_id)`
- **Description**: Retrieves all destinations (outputs) for a given worker group.
- **Endpoint**: `/api/v1/m/{group_id}/system/outputs`
- **Args**:
    - `group_id` (str): The ID of the worker group.
- **Returns**: JSON response containing destinations.

#### `get_pipelines(self, group_id)`
- **Description**: Retrieves all pipelines for a given worker group.
- **Endpoint**: `/api/v1/m/{group_id}/pipelines`
- **Args**:
    - `group_id` (str): The ID of the worker group.
- **Returns**: JSON response containing pipelines.

### Helper Functions

#### `get_api_client_from_env()`
- **Description**: Creates a `CriblAPI` client using environment variables (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, `CRIBL_USERNAME`, `CRIBL_PASSWORD`).
- **Returns**: An instance of `CriblAPI`.

#### `get_cached_api_client()`
- **Description**: Returns a cached `CriblAPI` client, initializing it if necessary.
- **Returns**: The cached `CriblAPI` instance.

## `graph_generator.py`

Logic to transform API data into a Graphviz graph.

### Functions

#### `generate_graph(api_client)`
- **Description**: Fetches Cribl configurations from the API and returns a graphviz `Digraph` object.
- **Args**:
    - `api_client` (CriblAPI): An instance of the `CriblAPI` client.
- **Returns**: `graphviz.Digraph` object representing the pipeline configuration.
- **Raises**: `Exception` if no worker groups are found.
