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
For detailed information on the Cribl API usage, refer to the local documentation files:
- [Cribl API Introduction](./cribl_api_intro.md)
- [Cribl API Update Configs](./cribl_api_update_configs.md)
- [Cribl API Authentication](./cribl_api_authentication.md)

The OpenAPI definition is available at:
- [cribl-apidocs-4.15.1-1b453caa.yml](./cribl-apidocs-4.15.1-1b453caa.yml)
