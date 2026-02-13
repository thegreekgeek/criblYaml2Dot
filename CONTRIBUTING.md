# Contributing to Cribl Pipeline Visualizer

Thank you for your interest in contributing to the Cribl Pipeline Visualizer project! We welcome contributions from the community to help improve this tool.

## Development Workflow

1.  **Fork the Repository**: specific to your own GitHub account.
2.  **Clone the Repository**: Clone your fork to your local machine.
    ```bash
    git clone https://github.com/your-username/cribl-pipeline-visualizer.git
    cd cribl-pipeline-visualizer
    ```
3.  **Create a Branch**: Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature/my-new-feature
    ```
4.  **Make Changes**: Implement your changes.
5.  **Test**: Run the test suite to ensure everything is working correctly.
6.  **Commit**: Commit your changes with a descriptive message.
7.  **Push**: Push your branch to your fork.
8.  **Pull Request**: Open a Pull Request (PR) against the main repository.

## Local Development Setup

To set up your local development environment:

1.  **Prerequisites**: Ensure you have Python 3.9+ and Graphviz installed.
    -   Ubuntu/Debian: `sudo apt-get install graphviz`
    -   macOS: `brew install graphviz`

2.  **Virtual Environment**: Create and activate a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Dependencies**: Install the required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**: Create a `.env` file based on `.env.example`.
    ```bash
    cp .env.example .env
    # Edit .env with your Cribl API details
    ```

5.  **Run the Application**:
    ```bash
    python app.py
    ```

## Running Tests

We use the `unittest` framework for testing. Please ensure all tests pass before submitting your PR.

To run the full test suite:

```bash
python -m unittest discover tests
```

To run a specific test file:

```bash
python -m unittest tests/test_cribl_api.py
```

## Code Style

*   **Python**: Follow PEP 8 guidelines.
*   **Documentation**: Ensure all new functions and classes have docstrings. Update `docs/CODE_REFERENCE.md` if you modify the API or architecture.
*   **Comments**: Write clear and concise comments where necessary.

## Docker

If you prefer to develop or test using Docker:

1.  Build the image:
    ```bash
    docker-compose build
    ```

2.  Run the container:
    ```bash
    docker-compose up
    ```

The application will be available at `http://localhost:8080`.

## Reporting Issues

If you find a bug or have a feature request, please open an issue in the GitHub repository. Provide as much detail as possible, including steps to reproduce the issue.
