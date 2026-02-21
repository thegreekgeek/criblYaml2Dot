# Cribl Pipeline Visualizer

A Flask application that visualizes Cribl Stream pipelines and their connections using Graphviz. It connects to the Cribl API to fetch configuration data and generates a dynamic graph showing inputs, outputs, and their pipeline connections.

## Features

*   **Dynamic Visualization**: Automatically generates a visual representation of your Cribl pipelines.
*   **Real-time Data**: Fetches the latest configuration directly from your Cribl Stream instance.
*   **Visual Clarity**: Uses Graphviz to layout nodes (inputs, outputs) and edges (pipelines) clearly.
*   **Dockerized**: Easy to deploy using Docker and Docker Compose.

## Prerequisites

*   **Python 3.9+** (for local development)
*   **Graphviz** (system dependency, required for rendering graphs)
    *   Ubuntu/Debian: `sudo apt-get install graphviz`
    *   macOS: `brew install graphviz`
*   **Cribl Stream**: A running instance of Cribl Stream (distributed or single instance).

## Project Structure

*   `app.py`: The main Flask application entry point.
*   `cribl_api.py`: Client library for interacting with the Cribl API.
*   `graph_generator.py`: Logic to transform API data into a Graphviz graph.
*   `templates/`: HTML templates for the web interface.
*   `tests/`: Unit tests for the application.
*   `AGENTS.md`: Documentation for AI agents working on this repo.

## Installation & Usage

### 1. Configuration

The application is configured using environment variables. You can set these in your shell or create a `.env` file (see `.env.example`).

| Variable | Description | Default |
| :--- | :--- | :--- |
| `CRIBL_BASE_URL` | The base URL of your Cribl Stream API. | `http://localhost:9000` |
| `CRIBL_AUTH_TOKEN` | Your Cribl authentication token (Recommended). | *(Empty)* |
| `CRIBL_USERNAME` | Username for auth (used if token is missing). | *(Empty)* |
| `CRIBL_PASSWORD` | Password for auth (used if token is missing). | *(Empty)* |

**Authentication Note**: If `CRIBL_AUTH_TOKEN` is provided, it takes precedence. Otherwise, the application attempts to log in using `CRIBL_USERNAME` and `CRIBL_PASSWORD`.

### 2. Running Locally

1.  Clone the repository and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Ensure Graphviz is installed on your system (see Prerequisites).

3.  Set your environment variables (e.g., in a `.env` file):
    ```bash
    export CRIBL_BASE_URL="http://my-cribl-instance:9000"
    export CRIBL_AUTH_TOKEN="your-token"
    ```

4.  Run the application:
    ```bash
    python app.py
    ```

5.  Access the application at **`http://localhost:5000`**.

### 3. Running with Docker

1.  Build and start the container using Docker Compose:
    ```bash
    docker-compose up --build
    ```

    *Note: The `docker-compose.yml` file maps port 5000 inside the container to port **8080** on your host.*

2.  Access the application at **`http://localhost:8080`**.

## Testing

To run the unit tests:

```bash
python -m unittest discover tests
```

## Troubleshooting

*   **Graphviz Executable Not Found**:
    *   Ensure Graphviz is installed on your system (`dot -V`).
    *   If running locally, make sure the `bin` directory of Graphviz is in your system's `PATH`.

*   **401 Unauthorized**:
    *   Check your `CRIBL_AUTH_TOKEN` or username/password combinations.
    *   Ensure the `CRIBL_BASE_URL` is reachable and correct.

*   **Connection Errors**:
    *   If running in Docker and connecting to a Cribl instance on the host machine, you may need to use `http://host.docker.internal:9000` as the `CRIBL_BASE_URL`.

## API Reference

This repository includes local copies of Cribl API documentation for reference:

*   [Cribl API Introduction](./docs/cribl_api_intro.md)
*   [Authentication](./docs/cribl_api_authentication.md)
*   [Update Configurations](./docs/cribl_api_update_configs.md)
*   [OpenAPI Definition](./docs/cribl-apidocs-4.15.1-1b453caa.yml)

## Documentation

For detailed technical documentation of the codebase, including class references and logic, please see:

*   [Architecture Overview](docs/ARCHITECTURE.md)
*   [Code Reference](docs/CODE_REFERENCE.md)

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to set up your development environment, run tests, and submit pull requests.

## Agents Documentation

For instructions and context relevant to AI agents working on this repository, please refer to [AGENTS.md](AGENTS.md).
