# Cribl Pipeline Visualizer Documentation for Agents

This document provides instructions and context for AI agents working on this repository.

## Project Overview

The **Cribl Pipeline Visualizer** is a Flask application that visualizes Cribl Stream pipelines and their connections using Graphviz. It connects to the Cribl API to fetch configuration data and generates a dynamic graph showing inputs, outputs, and their pipeline connections.

## Key Documentation

*   **[Architecture Overview](docs/ARCHITECTURE.md)**: High-level system design and data flow.
*   **[Code Reference](docs/CODE_REFERENCE.md)**: Detailed technical documentation of classes and functions.
*   **[Contributing Guidelines](CONTRIBUTING.md)**: Development workflow and standards.

## Project Structure

*   `app.py`: The main Flask application.
*   `cribl_api.py`: Client library for interacting with the Cribl API.
*   `graph_generator.py`: Logic to transform API data into a Graphviz graph.
*   `templates/`: HTML templates.
*   `tests/`: Unit tests.

## Development & Testing

*   **Dependencies**: `pip install -r requirements.txt`. Requires system `graphviz`.
*   **Testing**: Run `python -m unittest discover tests`.
*   **Running**: `python app.py` (Locally) or `docker-compose up` (Docker).

## Agent Guidelines

1.  **Context**: Always refer to `docs/ARCHITECTURE.md` and `docs/CODE_REFERENCE.md` before making changes.
2.  **API Client**: The `CriblAPI` class handles authentication. If modified, ensure token management is preserved.
3.  **Graph Generation**: `graphviz` produces DOT source. Ensure generated labels are properly escaped and formatted.
4.  **Tests**: All new features must include unit tests. Run existing tests to ensure no regressions.
5.  **Documentation**: Update `README.md`, `AGENTS.md`, and `docs/` files if you modify the system behavior.

## Symbolic Links

*   `GEMINI.md` and `QWEN.md` are symbolic links to this file. Do not delete or overwrite them with regular files.
