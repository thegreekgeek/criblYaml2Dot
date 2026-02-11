# Cribl Pipeline Visualizer Documentation for Agents

This document provides instructions and context for AI agents working on this repository.

## Project Overview

The **Cribl Pipeline Visualizer** is a Flask application that visualizes Cribl Stream pipelines and their connections using Graphviz. It connects to the Cribl API to fetch configuration data (inputs, outputs, pipelines) and generates a dynamic graph.

## Architecture

*   **`app.py`**: The main Flask application. It defines the routes and serves the generated SVG. It uses a cached `CriblAPI` client.
*   **`cribl_api.py`**: A client library for interacting with the Cribl API. It handles authentication and fetching worker groups, sources, destinations, and pipelines.
*   **`graph_generator.py`**: Contains the logic to transform the data fetched from the API into a Graphviz `Digraph` object.
*   **`templates/index.html`**: The HTML template used to display the generated SVG graph.

## Environment & Dependencies

*   **Python 3.9+**
*   **Flask**: Web framework.
*   **Graphviz**: Python library for graph creation. **Note:** The system-level `graphviz` package must also be installed (e.g., `apt-get install graphviz`).
*   **Requests**: For making API calls.
*   **Docker**: The application is containerized. `Dockerfile` and `docker-compose.yml` are provided.

## Running the Application

### Locally

1.  Create a `.env` file based on `.env.example` and set your Cribl credentials (`CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN` or `CRIBL_USERNAME`/`CRIBL_PASSWORD`).
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Run: `python app.py`.
4.  Access at `http://localhost:5000`.

### With Docker

1.  Run `docker-compose up --build`.
2.  Access at `http://localhost:8080`.

## Testing

Unit tests are located in the `tests/` directory.

To run tests:
```bash
python -m unittest discover tests
```

*   `tests/test_graph_generator.py`: Tests the graph generation logic using mocked API responses.
*   `tests/test_cribl_api.py`: Tests the API client methods (mocking `requests`).

## Key Considerations for Agents

*   **API Client**: The `CriblAPI` class handles authentication. If you modify it, ensure you handle token management and headers correctly.
*   **Graphviz**: When modifying graph generation, remember that the `graphviz` library produces DOT source code. Ensure compatibility with standard Graphviz rendering.
*   **Documentation**: Keep `README.md` and this file updated if you add new features or change the architecture.
*   **Symlinks**: `GEMINI.md` and `QWEN.md` are symbolic links to this file and should be maintained as such.
# AGENTS DOCUMENT

## Objective
The current objective is to maintain and enhance a Python-based Flask application that visualizes Cribl Stream pipelines. The application retrieves configuration data (inputs, outputs, and pipeline connections) from the Cribl API and generates a Graphviz visualization.

## Tooling
- **Python 3.9+**: The core programming language.
- **Flask**: Web framework used to serve the visualization.
- **Graphviz**: Used for generating the pipeline graph.
- **Requests**: For interacting with the Cribl API.
- **Docker & Docker Compose**: For containerizing and deploying the application.

## Project Structure & Goals
The project has evolved from a local file-based script to a fully dockerized web application interacting with the Cribl API.

### Current Features
- **API Integration**: `cribl_api.py` handles authentication and data fetching from Cribl Stream.
- **Graph Generation**: `graph_generator.py` transforms the API data into a DOT format graph.
- **Web Interface**: `app.py` serves the generated graph as an SVG.
- **Containerization**: The app is dockerized and can be deployed via `docker-compose`.

### Future Goals / Maintenance
- Maintain API compatibility with newer Cribl Stream versions.
- Enhance visualization features (e.g., more detailed node information, interactive graphs).
- Ensure robust error handling and logging.

## Additional Documentation
For detailed technical documentation of the codebase, refer to:
- [Code Reference](./docs/CODE_REFERENCE.md)

For detailed information on the Cribl API usage, refer to the local documentation files:
- [Cribl API Introduction](./docs/cribl_api_intro.md)
- [Cribl API Update Configs](./docs/cribl_api_update_configs.md)
- [Cribl API Authentication](./docs/cribl_api_authentication.md)

The OpenAPI definition is available at:
- [cribl-apidocs-4.15.1-1b453caa.yml](./docs/cribl-apidocs-4.15.1-1b453caa.yml)
