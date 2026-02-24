# Architecture Overview

This document provides a high-level overview of the Cribl Pipeline Visualizer architecture, explaining the system components, data flow, and deployment strategy.

## System Components

The application is built using Python and consists of the following key components:

### 1. Flask Application (`app.py`)
-   **Role**: The web server and entry point.
-   **Responsibilities**:
    -   Handling HTTP requests (currently only the root `/` route).
    -   Orchestrating the data retrieval and graph generation process.
    -   Rendering the final SVG graph within an HTML template.
    -   Caching the API client instance to minimize authentication overhead.

### 2. Cribl API Client (`cribl_api.py`)
-   **Role**: The interface to the Cribl Stream API.
-   **Responsibilities**:
    -   Authentication (handling tokens and login credentials).
    -   Fetching configuration data:
        -   Worker Groups (`/api/v1/master/groups`)
        -   Inputs (`/api/v1/m/{group_id}/system/inputs`)
        -   Outputs (`/api/v1/m/{group_id}/system/outputs`)
        -   Pipelines (`/api/v1/m/{group_id}/pipelines`) - *Note: Fetched but not currently used in graph generation.*
    -   Managing the HTTP session and headers.

### 3. Graph Generator (`graph_generator.py`)
-   **Role**: The visualization logic.
-   **Responsibilities**:
    -   Transforming the raw configuration data from the API into a Graphviz `Digraph` object.
    -   Defining the visual style of nodes (Inputs: Light Blue, Outputs: Light Green) and edges.
    -   Handling node descriptions and ensuring correct label formatting.
    -   Grouping nodes by Worker Group using subgraphs.

## Data Flow

1.  **User Request**: A user accesses the application URL (e.g., `http://localhost:8080`).
2.  **API Client Initialization**: The application checks for a cached `CriblAPI` instance. If none exists, it initializes one using environment variables (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, etc.).
3.  **Data Retrieval**:
    -   The application calls `generate_graph(api_client)`.
    -   The `api_client` fetches the list of Worker Groups.
    -   For each group, it fetches the configured Inputs and Outputs.
4.  **Graph Construction**:
    -   `graph_generator` iterates through the data.
    -   It creates nodes for each enabled Input and Output.
    -   It inspects the `connections` property of each Input to determine which Output it sends data to.
    -   It creates directed edges representing these pipeline connections.
5.  **Rendering**:
    -   The resulting Graphviz object is piped to an SVG string.
    -   The SVG is embedded into the `index.html` template.
6.  **Response**: The rendered HTML page is sent back to the user's browser.

## Deployment

The application is designed to be containerized using Docker.

-   **Dockerfile**: Builds a Python 3.9-slim image, installs system dependencies (Graphviz), and sets up the Python environment.
-   **Docker Compose**: Orchestrates the container, mapping port 5000 (container) to 8080 (host) and injecting environment variables.

This setup ensures consistency across different environments and simplifies deployment.
