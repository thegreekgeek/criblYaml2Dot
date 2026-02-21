# Architecture Overview

This document provides a high-level overview of the Cribl Pipeline Visualizer architecture.

## System Overview

The Cribl Pipeline Visualizer is a web application designed to visualize the configuration of a Cribl Stream instance. It connects to the Cribl API, retrieves worker groups, inputs, outputs, and pipelines, and renders a directed graph using Graphviz.

## Components

The system consists of the following main components:

### 1. Flask Application (`app.py`)
The web server that handles user requests.
-   **Routes**: Serves the root endpoint `/`.
-   **Responsibility**: Orchestrates data fetching, graph generation, and rendering the final SVG to the user.
-   **Caching**: Maintains a cached instance of the API client to reuse authentication tokens and minimize API calls.

### 2. Cribl API Client (`cribl_api.py`)
A wrapper around the Cribl Stream REST API.
-   **Authentication**: Handles login and token management. It supports both username/password login and pre-generated authentication tokens.
-   **Data Retrieval**: Provides methods to fetch worker groups, inputs (sources), outputs (destinations), and pipelines.
-   **Session Management**: Uses `requests.Session` for efficient connection pooling and header management (e.g., `Authorization`).

### 3. Graph Generator (`graph_generator.py`)
The core logic for transforming Cribl configuration into a visual graph.
-   **Library**: Uses the `graphviz` Python library to generate DOT code.
-   **Logic**:
    -   Groups nodes by Worker Group.
    -   Filters out disabled inputs.
    -   Draws edges based on the `connections` property of inputs.
    -   Styles nodes (Inputs: lightblue box, Outputs: lightgreen box) and adds descriptions to labels if available.

### 4. Docker Environment
The application is fully containerized for easy deployment.
-   **Dockerfile**: Builds a Python environment based on `python:3.9-slim` with Graphviz installed.
-   **Docker Compose**: Orchestrates the container, manages environment variables, and maps host port 8080 to container port 5000.

## Data Flow

1.  **User Request**: A user visits the application in their browser (e.g., `http://localhost:8080`).
2.  **API Client Initialization**: The app checks for a cached `CriblAPI` client. If none exists, it initializes one using environment variables (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, etc.).
3.  **Data Fetching**:
    -   The app fetches the list of Worker Groups (`/api/v1/master/groups`).
    -   For each group, it fetches Inputs (`/api/v1/m/{group_id}/system/inputs`) and Outputs (`/api/v1/m/{group_id}/system/outputs`).
4.  **Graph Construction**:
    -   Nodes are created for each enabled Input and Output.
    -   Edges are created based on Input `connections`, labeled with the Pipeline name.
5.  **Rendering**:
    -   The `graphviz` library compiles the graph definition into SVG format.
6.  **Response**: The SVG is embedded in an HTML template (`index.html`) and returned to the user.

## Deployment

The application is designed to be deployed using Docker.
-   **Port Mapping**: Host port 8080 -> Container port 5000.
-   **Configuration**: All configuration is handled via environment variables passed to the container.
