# Code Reference

This document provides a technical reference for the Cribl Pipeline Visualizer codebase.

## app.py

The main Flask application entry point.

### Functions

#### `index()`
The main route (`/`) that generates and renders the graph.

**Returns:**
- `str`: Rendered HTML template with the graph SVG.

**Renders:**
- `index.html`: If graph generation is successful.
- `error.html`: If an exception occurs (e.g., API failure).

#### `get_cached_api_client()`
Returns a cached `CriblAPI` client, initializing it if necessary. This function ensures that the API client is reused across requests within the same worker.

## cribl_api.py

Client library for interacting with the Cribl API.

### Class: CriblAPI

Handles authentication and API requests.

#### `__init__(self, base_url="http://localhost:9000", username=None, password=None, token=None)`
Initializes the CriblAPI client. Authenticates and retrieves a token if username and password are provided.

**Args:**
- `base_url` (str): The base URL of the Cribl API. Defaults to `http://localhost:9000`.
- `username` (str, optional): The username for authentication.
- `password` (str, optional): The password for authentication.
- `token` (str, optional): An existing authentication token.

#### `login(self, username, password)`
Logs in to the Cribl API and retrieves an authentication token.

**Args:**
- `username` (str): The username.
- `password` (str): The password.

#### `get_worker_groups(self)`
Retrieves all worker groups. Assumes the endpoint is `/api/v1/master/groups`.

**Returns:**
- `dict`: JSON response containing worker groups.

#### `get_sources(self, group_id)`
Retrieves all sources (inputs) for a given worker group. Assumes the endpoint is `/api/v1/m/<group_id>/system/inputs`.

**Args:**
- `group_id` (str): The ID of the worker group.

**Returns:**
- `dict`: JSON response containing sources.

#### `get_destinations(self, group_id)`
Retrieves all destinations (outputs) for a given worker group. Assumes the endpoint is `/api/v1/m/<group_id>/system/outputs`.

**Args:**
- `group_id` (str): The ID of the worker group.

**Returns:**
- `dict`: JSON response containing destinations.

#### `get_pipelines(self, group_id)`
Retrieves all pipelines for a given worker group. Assumes the endpoint is `/api/v1/m/<group_id>/pipelines`.

**Args:**
- `group_id` (str): The ID of the worker group.

**Returns:**
- `dict`: JSON response containing pipelines.

#### Internal Methods
- `_post(self, endpoint, payload)`: Performs a POST request to the specified endpoint.
- `_get(self, endpoint)`: Performs a GET request to the specified endpoint.

### Helper Functions

#### `get_api_client_from_env()`
Creates a `CriblAPI` client from environment variables (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, `CRIBL_USERNAME`, `CRIBL_PASSWORD`).

#### `get_cached_api_client()`
Returns a cached `CriblAPI` client, initializing it if necessary using `get_api_client_from_env()`.

## graph_generator.py

Logic to transform API data into a Graphviz graph.

### Functions

#### `generate_graph(api_client)`
Fetches Cribl configurations from the API and returns a graphviz Digraph object.

**Args:**
- `api_client` (CriblAPI): An instance of the CriblAPI client.

**Returns:**
- `graphviz.Digraph`: The generated graph showing inputs, outputs, and pipeline connections.

**Raises:**
- `Exception`: If no worker groups are found.
