# Cribl Pipeline Visualizer Documentation for Agents

This document provides instructions and context for AI agents working on this repository.

## Project Overview

The **Cribl Pipeline Visualizer** is a Flask application that visualizes Cribl Stream pipelines and their connections using Graphviz. It connects to the Cribl API to fetch configuration data (inputs, outputs, pipelines) and generates a dynamic graph.

## Documentation Map

-   **Architecture**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for a system overview, component details, and data flow.
-   **Code Reference**: See [docs/CODE_REFERENCE.md](docs/CODE_REFERENCE.md) for detailed class and function documentation.
-   **Contribution**: See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow and guidelines.

## Key Components

*   **`app.py`**: The main Flask application. Serves the SVG graph.
*   **`cribl_api.py`**: Client library for interacting with the Cribl API. Handles authentication and data fetching.
*   **`graph_generator.py`**: Logic to transform API data into a Graphviz `Digraph` object.
*   **`templates/index.html`**: The HTML template used to display the generated SVG.

## Environment & Dependencies

*   **Python 3.9+**
*   **Flask**: Web framework.
*   **Graphviz**: Python library for graph creation. **Note:** The system-level `graphviz` package must also be installed (e.g., `apt-get install graphviz`).
*   **Requests**: For making API calls.
*   **Docker**: The application is containerized. `Dockerfile` and `docker-compose.yml` are provided.

## Running the Application

### Locally

1.  Create a `.env` file based on `.env.example`.
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
*   **Symlinks**: `GEMINI.md` and `QWEN.md` are symbolic links to this file and should be maintained as such.
*   **Documentation**: Keep `README.md`, `docs/ARCHITECTURE.md`, `docs/CODE_REFERENCE.md`, and this file updated if you add new features or change the architecture.
