# System Architecture

This document provides a high-level overview of the Cribl Pipeline Visualizer architecture.

## System Overview

The Cribl Pipeline Visualizer is a Flask-based web application designed to visualize the data flow within a Cribl Stream environment. It connects to the Cribl API to retrieve configuration details (inputs, outputs, and pipelines) and renders them as a directed graph using Graphviz.

## Components

### 1. Flask Application (`app.py`)
-   **Role**: Serves as the web server and entry point.
-   **Functionality**:
    -   Handles HTTP requests (root route `/`).
    -   Manages the `CriblAPI` client instance (caching it to avoid repeated logins).
    -   Invokes the graph generation logic.
    -   Renders the final SVG graph within an HTML template.

### 2. Cribl API Client (`cribl_api.py`)
-   **Role**: Handles all communication with the Cribl Stream API.
-   **Functionality**:
    -   **Authentication**: Supports token-based authentication and username/password login (retrieving a bearer token).
    -   **Data Retrieval**: Fetches worker groups, system inputs, system outputs, and pipelines.
    -   **Session Management**: Uses `requests.Session` for connection pooling and header management.

### 3. Graph Generator (`graph_generator.py`)
-   **Role**: Transforms Cribl configuration data into a visual graph.
-   **Functionality**:
    -   Uses the `graphviz` Python library to construct a `Digraph`.
    -   Iterates through worker groups to create subgraphs (clusters).
    -   Nodes: Represents inputs (blue box) and outputs (green box).
    -   Edges: Represents pipelines connecting inputs to outputs.
    -   **Filtering**: Excludes disabled inputs.

## Data Flow

1.  **User Request**: A user accesses the application URL (e.g., `http://localhost:8080`).
2.  **API Check**: The application checks for a cached `CriblAPI` client. If not present, it initializes one using environment variables.
3.  **Data Fetch**: The application calls `generate_graph`, which triggers the API client to fetch:
    -   Worker Groups
    -   Inputs (for each group)
    -   Outputs (for each group)
    -   Pipelines (implicit in input connections)
4.  **Graph Construction**:
    -   Nodes and edges are added to the Graphviz object based on the fetched configuration.
    -   Disabled inputs are skipped.
5.  **Rendering**:
    -   The Graphviz object is piped to an SVG string.
    -   The SVG is embedded in `index.html` and returned to the user's browser.

## Deployment

-   **Docker**: The application is containerized using a `Dockerfile`.
-   **Orchestration**: `docker-compose.yml` orchestrates the container, mapping port 8080 (host) to 5000 (container).
-   **Configuration**: Environment variables (e.g., `CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`) inject configuration into the container.
