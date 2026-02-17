# Cribl Pipeline Visualizer Documentation for Agents

This document provides instructions and context for AI agents working on this repository.

## Project Overview

The **Cribl Pipeline Visualizer** is a Flask application that visualizes Cribl Stream pipelines and their connections using Graphviz. It connects to the Cribl API to fetch configuration data (inputs, outputs, and pipelines) and generates a dynamic graph showing how data flows through the system.

## Architecture

The project has evolved from a local script to a dockerized web application.

*   **`app.py`**: The main Flask application entry point. It handles routes (`/`), manages the global `CriblAPI` client cache, and serves the generated SVG.
*   **`cribl_api.py`**: A client library for interacting with the Cribl API. It handles authentication (token management) and fetches worker groups, sources, destinations, and pipelines.
*   **`graph_generator.py`**: Contains the core logic to transform the API data into a Graphviz `Digraph` object. It handles node creation (inputs/outputs) and edge generation based on pipeline connections.
*   **`templates/index.html`**: The HTML template used to render the generated SVG graph.

## Environment & Dependencies

*   **Python 3.9+**: Core programming language.
*   **Flask**: Web framework for the interface.
*   **Graphviz**: Python library for graph creation. **Crucial:** The system-level `graphviz` package must also be installed (e.g., `apt-get install graphviz`).
*   **Requests**: For HTTP interactions with the Cribl API.
*   **Docker & Docker Compose**: For containerization and easy deployment.

## Running the Application

### Locally

1.  Create a `.env` file based on `.env.example`.
2.  Set your credentials: `CRIBL_BASE_URL` (default: `http://localhost:9000`), and either `CRIBL_AUTH_TOKEN` (recommended) or `CRIBL_USERNAME`/`CRIBL_PASSWORD`.
3.  Install dependencies: `pip install -r requirements.txt`.
4.  Run: `python app.py`.
5.  Access at `http://localhost:5000`.

### With Docker

1.  Run `docker-compose up --build`.
2.  Access at `http://localhost:8080` (mapped from container port 5000).

## Testing

Unit tests are located in the `tests/` directory.

To run tests:
```bash
python -m unittest discover tests
```

*   `tests/test_graph_generator.py`: Tests graph generation logic (mocking API responses).
*   `tests/test_cribl_api.py`: Tests API client methods (mocking `requests`).

## Key Considerations for Agents

*   **API Client**: The `CriblAPI` class handles authentication. Modifications should ensure token management and headers are handled correctly.
*   **Graphviz**: The `graphviz` library produces DOT source code. Ensure compatibility with standard Graphviz rendering.
*   **Documentation**: Keep `README.md` and this file updated if you add new features or change the architecture.
*   **Symlinks**: `GEMINI.md` and `QWEN.md` are symbolic links to this file and should be maintained as such.

## Future Goals / Maintenance

*   Maintain API compatibility with newer Cribl Stream versions.
*   Enhance visualization features (e.g., more detailed node information, interactive graphs).
*   Ensure robust error handling and logging.

## Additional Documentation

For internal code documentation and contribution guidelines:
- [Code Reference](./docs/CODE_REFERENCE.md)
- [Contributing Guidelines](./CONTRIBUTING.md)

For detailed information on the Cribl API usage, refer to the local documentation files:
- [Cribl API Introduction](./docs/cribl_api_intro.md)
- [Cribl API Update Configs](./docs/cribl_api_update_configs.md)
- [Cribl API Authentication](./docs/cribl_api_authentication.md)

The OpenAPI definition is available at:
- [cribl-apidocs-4.15.1-1b453caa.yml](./docs/cribl-apidocs-4.15.1-1b453caa.yml)
