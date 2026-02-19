# Architecture Overview

This document provides a high-level overview of the Cribl Pipeline Visualizer architecture.

## System Components

The application consists of the following key components:

1.  **Flask Web Application (`app.py`)**:
    *   Acts as the entry point and controller.
    *   Handles HTTP requests from the user.
    *   Manages the application lifecycle and configuration.
    *   Orchestrates the data fetching and graph generation process.
    *   Serves the final SVG visualization to the user.

2.  **Cribl API Client (`cribl_api.py`)**:
    *   Encapsulates all communication with the Cribl Stream API.
    *   Handles authentication (token management, login).
    *   Provides high-level methods to fetch worker groups, inputs, outputs, and pipelines.
    *   Uses `requests.Session` for connection pooling and header management.
    *   Automatically manages the authentication token, ensuring subsequent requests are authorized.

3.  **Graph Generator (`graph_generator.py`)**:
    *   Contains the core business logic for visualization.
    *   Transforms raw JSON configuration data from Cribl into a Graphviz `Digraph` object.
    *   Defines the visual style (nodes, edges, colors, layout) of the pipeline graph.
    *   Filters out disabled inputs to keep the visualization clean.

4.  **Templates (`templates/`)**:
    *   `index.html`: Displays the generated SVG graph.
    *   `error.html`: Displays error messages in case of failures.

## Data Flow

1.  **User Request**: A user accesses the application root URL (`/`).
2.  **Initialization**: `app.py` initializes the `CriblAPI` client (using a cached instance if available via `get_cached_api_client()`).
3.  **Data Retrieval**:
    *   The app calls `generate_graph(api_client)`.
    *   `graph_generator.py` calls `api_client.get_worker_groups()` to get the list of worker groups.
    *   For each group, it calls `api_client.get_sources(group_id)` and `api_client.get_destinations(group_id)`.
4.  **Graph Construction**:
    *   `graph_generator.py` processes the inputs and outputs.
    *   It creates nodes for each enabled input (blue) and output (green).
    *   It iterates through input connections to create edges representing pipelines.
    *   A `graphviz.Digraph` object is constructed.
5.  **Rendering**:
    *   The `Digraph` object is piped to SVG format (`dot.pipe(format="svg")`).
    *   The SVG string is passed to `index.html`.
6.  **Response**: The rendered HTML page containing the pipeline visualization is sent back to the user.

## Deployment

The application is containerized using Docker.
*   **Dockerfile**: Builds a Python 3.9 slim image, installs system dependencies (Graphviz), and application dependencies.
*   **Docker Compose**: Orchestrates the container, mapping port 8080 (host) to 5000 (container) and injecting environment variables.
