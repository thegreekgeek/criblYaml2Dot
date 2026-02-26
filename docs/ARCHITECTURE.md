# Architecture Overview

This document provides a high-level overview of the Cribl Pipeline Visualizer architecture.

## System Overview

The Cribl Pipeline Visualizer is a web-based application designed to provide a graphical representation of Cribl Stream pipelines. It connects to a live Cribl Stream instance, retrieves configuration data, and dynamically generates a visual graph of inputs, outputs, and their interconnections.

## Components

The application is built using Python and consists of the following key components:

### 1. Flask Application (`app.py`)
*   **Role**: The web server and entry point for the application.
*   **Responsibilities**:
    *   Handling HTTP requests (specifically the root route `/`).
    *   Managing the application lifecycle and configuration via environment variables.
    *   Orchestrating the data fetching and graph generation process.
    *   Serving the final SVG visualization to the user.
    *   Basic error handling and displaying error pages.

### 2. Cribl API Client (`cribl_api.py`)
*   **Role**: The interface for communicating with the Cribl Stream API.
*   **Responsibilities**:
    *   **Authentication**: Handling login and token management. It supports both token-based and username/password authentication.
    *   **Data Retrieval**: Fetching worker groups, inputs (sources), and outputs (destinations) from the Cribl instance.
    *   **Session Management**: Using `requests.Session` to maintain persistent connections and headers.

### 3. Graph Generator (`graph_generator.py`)
*   **Role**: The transformation engine that converts raw API data into a visual graph.
*   **Responsibilities**:
    *   Processing the JSON data returned by the API client.
    *   Constructing a `graphviz.Digraph` object.
    *   Defining nodes for inputs and outputs with appropriate styling.
    *   Creating edges to represent pipeline connections between inputs and outputs.
    *   Organizing the graph using subgraphs (clusters) for each worker group.

### 4. Frontend (`templates/`)
*   **Role**: The presentation layer.
*   **Responsibilities**:
    *   `index.html`: Displays the generated SVG graph.
    *   `error.html`: Displays error messages if the backend fails to generate the graph.

## Data Flow

1.  **User Request**: A user accesses the application URL (e.g., `http://localhost:8080/`).
2.  **API Client Initialization**: The Flask app retrieves or initializes a cached `CriblAPI` client.
3.  **Data Fetching**: The app calls the API client to fetch the list of worker groups.
4.  **Graph Construction**: For each worker group, the `graph_generator` fetches inputs and outputs, then iterates through them to build the graph nodes and edges.
5.  **Rendering**: The `graphviz` library compiles the graph into SVG format.
6.  **Response**: The Flask app injects the SVG into the `index.html` template and returns the rendered HTML to the user's browser.

## Deployment Strategy

The application is designed to be deployed as a Docker container.

*   **Docker**: A `Dockerfile` is provided to build a lightweight image based on `python:3.9-slim`. It installs system dependencies (Graphviz) and Python requirements.
*   **Docker Compose**: A `docker-compose.yml` file orchestrates the deployment, mapping ports and managing environment variables.
*   **Configuration**: The system is configured entirely via environment variables (e.g., `CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`), making it suitable for various deployment environments (local, dev, prod).
