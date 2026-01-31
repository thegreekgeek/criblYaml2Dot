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

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  Set up a virtual environment (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application is configured using environment variables. You can set these in your shell or create a `.env` file (copy from `.env.example` if available).

| Variable | Description | Default (Local) | Default (Docker) |
| :--- | :--- | :--- | :--- |
| `CRIBL_BASE_URL` | The base URL of your Cribl Stream API. | `http://localhost:9000` | `http://host.docker.internal:9000` |
| `CRIBL_AUTH_TOKEN` | Your Cribl authentication token. | *(Empty)* | *(Empty)* |
| `CRIBL_USERNAME` | Username for auth (if token not provided). | *(Empty)* | *(Empty)* |
| `CRIBL_PASSWORD` | Password for auth (if token not provided). | *(Empty)* | *(Empty)* |

## Usage

### Running Locally

1.  Set the environment variables or create a `.env` file:
    ```bash
    cp .env.example .env
    # Edit .env with your credentials
    ```
    Or manually export them:
    ```bash
    export CRIBL_BASE_URL="http://my-cribl-instance:9000"
    export CRIBL_USERNAME="admin"
    export CRIBL_PASSWORD="password"
    ```

2.  Run the application:
    ```bash
    python app.py
    ```

3.  Open your browser and navigate to `http://localhost:5000`.

### Running with Docker

1.  Build and start the container using Docker Compose:
    ```bash
    docker-compose up --build
    ```

    *Note: The `docker-compose.yml` file is configured to look for a `.env` file. It also sets `CRIBL_BASE_URL` to `http://host.docker.internal:9000` by default, which allows the container to access Cribl running on the host machine.*

2.  Access the application at `http://localhost:8080`.

## Testing

To run the unit tests:

```bash
python -m unittest discover tests
```

## Agents Documentation

For instructions and context relevant to AI agents working on this repository, please refer to [AGENTS.md](AGENTS.md).
