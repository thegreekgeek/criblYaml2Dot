# Contributing to Cribl Pipeline Visualizer

Thank you for your interest in contributing to the Cribl Pipeline Visualizer project! We welcome contributions, bug reports, and feature requests.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.9+**: The project is built with Python.
*   **Graphviz**: Required for rendering the graph. You must install the system package.
    *   Ubuntu/Debian: `sudo apt-get install graphviz`
    *   macOS: `brew install graphviz`
*   **Docker** (Optional): For running the application in a container.

## Setting Up the Development Environment

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/cribl-pipeline-visualizer.git
    cd cribl-pipeline-visualizer
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables**:
    Copy the example configuration file and update it with your Cribl credentials.
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and set `CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN` (or `CRIBL_USERNAME` and `CRIBL_PASSWORD`).

## Running the Application Locally

To start the Flask development server:

```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## Running with Docker

To build and run the application using Docker Compose:

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8080`.

## Running Tests

We use `unittest` for testing. To run the test suite:

```bash
python -m unittest discover tests
```

Please ensure all tests pass before submitting a pull request.

## Code Style

*   Follow PEP 8 guidelines for Python code.
*   Write clear and concise docstrings for all functions and classes.
*   Keep functions focused on a single responsibility.

## Submission Process

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix (`git checkout -b feature/new-feature`).
3.  Commit your changes with descriptive messages.
4.  Push your branch to your fork (`git push origin feature/new-feature`).
5.  Open a Pull Request against the `main` branch.
6.  Ensure your PR description clearly explains the changes and references any related issues.

## Reporting Issues

If you encounter any bugs or have suggestions for improvements, please open an issue on GitHub.
