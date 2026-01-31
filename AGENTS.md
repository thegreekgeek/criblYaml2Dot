# AGENTS DOCUMENT

## Objective
The goal of this project is to provide a visualization tool for Cribl Stream pipelines. The application connects to the Cribl Stream API, retrieves the configuration of inputs, pipelines, and outputs, and generates a Graphviz graph to visualize the data flow.

## Tooling
*   **Python**: Core programming language.
*   **Flask**: Web framework for serving the visualization.
*   **Graphviz**: Visualization library.
*   **Docker**: For containerized deployment.

## Project State
The application is fully functional, API-based, and Dockerized.

### Completed Goals
*   Application connects to Cribl API to fetch configuration.
*   Generates DOT files and renders SVG graphs.
*   Dockerized with `Dockerfile` and `docker-compose.yml`.

### Current Focus
*   Maintenance and bug fixes.
*   Documentation updates.
*   Improving graph layout and readability.

## Additional Documentation
*   [Cribl API Introduction](./cribl_api_intro.md)
*   [Cribl API Update Configs](./cribl_api_update_configs.md)
*   [Cribl API Authentication](./cribl_api_authentication.md)

Cribl Stream APIdocs are available in [cribl-apidocs-4.15.1-1b453caa.yml](./cribl-apidocs-4.15.1-1b453caa.yml).
