# AGENTS DOCUMENT

## Objective
This project is a Flask application that visualizes Cribl Stream pipelines and their connections using Graphviz. It connects to the Cribl API to fetch configuration data and generates a dynamic graph.

## Current State
The application is fully implemented as a Dockerized Flask app. It uses the Cribl API to fetch worker groups, inputs, and outputs.

## Tooling
- **Language**: Python 3.9+
- **Framework**: Flask
- **Libraries**: `requests` for API interaction, `graphviz` for graph generation, `python-dotenv` for configuration.
- **Testing**: `unittest`

## Maintenance & Development
- **Code Style**: Follow standard Python conventions (PEP 8). Ensure code is documented with docstrings.
- **Testing**: Run tests with `python -m unittest discover tests` before submitting changes. Ensure new features have corresponding tests.
- **Configuration**: Use `.env` for local development. Do not hardcode credentials.
- **Docker**: Maintain `Dockerfile` and `docker-compose.yml` for deployment.

## Additional Documentation
- [Cribl API Introduction](./cribl_api_intro.md)
- [Cribl API Update Configs](./cribl_api_update_configs.md)
- [Cribl API Authentication](./cribl_api_authentication.md)
- [Cribl Stream APIdocs](./cribl-apidocs-4.15.1-1b453caa.yml)
