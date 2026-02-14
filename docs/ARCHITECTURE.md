# Architecture

This document describes the high-level architecture of the Cribl Pipeline Visualizer application.

## Overview

The application is a Python-based web service that connects to a Cribl Stream instance, retrieves its configuration, and generates a visual representation of the data flow. It is built using Flask and Graphviz.

## Architecture Diagram

The following diagram illustrates the request flow and component interactions:

```mermaid
graph TD
    User[User Browser] -- HTTP GET / --> FlaskApp[Flask Application (app.py)]

    subgraph "Application Container"
        FlaskApp -- 1. Get Client --> CriblAPI[CriblAPI Client (cribl_api.py)]
        CriblAPI -- 2. Auth/Fetch Data --> CriblStream[Cribl Stream API]
        CriblStream -- JSON Config --> CriblAPI
        FlaskApp -- 3. Generate Graph --> GraphGen[Graph Generator (graph_generator.py)]
        GraphGen -- DOT Source --> Graphviz[Graphviz Engine]
        Graphviz -- SVG --> FlaskApp
        FlaskApp -- Render Template --> User
    end
```

## Request Flow

1.  **User Request**: The user accesses the root URL (`/`) via a web browser.
2.  **API Client Retrieval**: The `app.py` module retrieves a cached instance of the `CriblAPI` client. If it doesn't exist, it initializes one using environment variables (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, etc.).
3.  **Data Fetching**: The `CriblAPI` client authenticates with the Cribl Stream instance (if necessary) and fetches:
    -   Worker Groups (`/api/v1/master/groups`)
    -   Inputs for each group (`/api/v1/m/{group}/system/inputs`)
    -   Outputs for each group (`/api/v1/m/{group}/system/outputs`)
    -   (Pipelines are available but not currently used for graph generation)
4.  **Graph Generation**: The `graph_generator.py` module processes the fetched data:
    -   It creates a Graphviz `Digraph` object.
    -   It iterates through worker groups, creating subgraphs.
    -   It creates nodes for inputs (blue) and outputs (green).
    -   It creates edges based on the `connections` property of input objects, labeling them with the pipeline name.
5.  **Rendering**: The `Digraph` object is piped to the `dot` executable to generate an SVG string.
6.  **Response**: The SVG string is embedded in the `index.html` template and returned to the user.

## Key Components

### `app.py`
The entry point for the Flask application. It handles routing, API client caching, and error handling. It renders the `index.html` template with the generated SVG.

### `cribl_api.py`
Encapsulates all interactions with the Cribl Stream API. It handles:
-   Authentication (Token-based or Username/Password)
-   Session management (Connection pooling)
-   Data retrieval methods (`get_worker_groups`, `get_sources`, `get_destinations`)

### `graph_generator.py`
Contains the business logic for transforming Cribl configuration data into a visual graph. It uses the `graphviz` Python library to construct the graph structure.

### `templates/index.html`
A simple HTML template that displays the generated SVG. It provides a container for the graph and basic styling.

## Deployment

The application is containerized using Docker.
-   **Dockerfile**: Builds the Python environment and installs system dependencies (Graphviz).
-   **docker-compose.yml**: Orchestrates the container, mapping port 8080 (host) to 5000 (container) and managing environment variables.
