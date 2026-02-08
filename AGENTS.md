# Cribl Pipeline Visualizer: Agents Documentation

This document provides instructions, context, and guidelines for AI agents working on this repository.

## Project Overview

The **Cribl Pipeline Visualizer** is a Flask application designed to visualize Cribl Stream pipelines and their connections. It dynamically generates a directed graph using Graphviz by fetching configuration data (inputs, outputs, and pipeline connections) directly from the Cribl API.

## Architecture

The application is structured into three main components:

*   **`app.py`**: The Flask web server. It handles HTTP requests, initializes the API client, and serves the rendered SVG graph to the user.
*   **`cribl_api.py`**: The API client library. It manages authentication (token/login) and encapsulates all HTTP requests to the Cribl Stream API to fetch worker groups, sources, destinations, and pipelines.
*   **`graph_generator.py`**: The visualization logic. It processes the data retrieved by the API client and constructs a Graphviz `Digraph` object representing the pipeline topology.

For a detailed breakdown of classes and functions, refer to **[docs/CODE_REFERENCE.md](docs/CODE_REFERENCE.md)**.

## Environment & Dependencies

*   **Language**: Python 3.9+
*   **Web Framework**: Flask
*   **Visualization**: Graphviz (requires both the `graphviz` Python library and the system-level `graphviz` package).
*   **HTTP Client**: Requests
*   **Containerization**: Docker and Docker Compose.

## Running the Application

### Local Development

1.  **Configuration**: Create a `.env` file based on `.env.example`.
    *   Set `CRIBL_BASE_URL` (default: `http://localhost:9000`).
    *   Set authentication credentials: `CRIBL_AUTH_TOKEN` (preferred) or `CRIBL_USERNAME` and `CRIBL_PASSWORD`.
2.  **Dependencies**: Install Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    *Ensure `graphviz` is installed on your OS (e.g., `apt-get install graphviz`).*
3.  **Run**:
    ```bash
    python app.py
    ```
4.  **Access**: Open `http://localhost:5000` in your browser.

### Docker Deployment

1.  **Build & Run**:
    ```bash
    docker-compose up --build
    ```
2.  **Access**: Open `http://localhost:8080` in your browser (mapped from container port 5000).

## Testing

Unit tests are located in the `tests/` directory.

*   **Command**:
    ```bash
    python -m unittest discover tests
    ```
*   **Scope**:
    *   `tests/test_graph_generator.py`: Verifies graph structure and logic using mocked data.
    *   `tests/test_cribl_api.py`: Verifies API client methods and authentication handling (mocks `requests`).

## Key Considerations for Agents

*   **API Client**: The `CriblAPI` class handles authentication state. When modifying it, ensure token management (Bearer prefix) and error handling (401 Unauthorized) are robust.
*   **Graphviz Compatibility**: The application generates DOT source code. Ensure any changes to graph properties are compatible with standard Graphviz rendering engines.
*   **Documentation Maintenance**:
    *   Update `docs/CODE_REFERENCE.md` if you modify function signatures or class structures.
    *   Update this file if you change the architecture or build process.
*   **Symbolic Links**: `GEMINI.md` and `QWEN.md` are symbolic links to this file (`AGENTS.md`) and **must be maintained** as such. Do not replace them with regular files.

## Additional Resources

*   **Internal Code Reference**: [docs/CODE_REFERENCE.md](docs/CODE_REFERENCE.md)
*   **Cribl API Docs**:
    *   [Introduction](./docs/cribl_api_intro.md)
    *   [Authentication](./docs/cribl_api_authentication.md)
    *   [Update Configs](./docs/cribl_api_update_configs.md)
    *   [OpenAPI Spec](./docs/cribl-apidocs-4.15.1-1b453caa.yml)
