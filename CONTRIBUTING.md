# Contributing to Cribl Pipeline Visualizer

Thank you for your interest in contributing to the Cribl Pipeline Visualizer! We welcome contributions from the community to help improve this project.

## Getting Started

1.  **Fork the repository**: Click the "Fork" button on the GitHub page to create your own copy of the repository.
2.  **Clone your fork**:
    ```bash
    git clone https://github.com/your-username/cribl-pipeline-visualizer.git
    cd cribl-pipeline-visualizer
    ```

## Environment Setup

1.  **Prerequisites**:
    *   Python 3.9+
    *   Graphviz (System package)
        *   Ubuntu/Debian: `sudo apt-get install graphviz`
        *   macOS: `brew install graphviz`

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    Copy the example environment file and configure it with your Cribl Stream credentials.
    ```bash
    cp .env.example .env
    ```
    Edit `.env` to set `CRIBL_BASE_URL`, `CRIBL_AUTH_TOKEN`, etc.

## Running the Application

*   **Locally**:
    ```bash
    python app.py
    ```
    Access at `http://localhost:5000`.

*   **With Docker**:
    ```bash
    docker-compose up --build
    ```
    Access at `http://localhost:8080`.

## Running Tests

We use `unittest` for testing. Please ensure all tests pass before submitting your changes.

```bash
python -m unittest discover tests
```

## Code Style

*   Follow PEP 8 guidelines for Python code.
*   Ensure docstrings are provided for new functions and classes.
*   Keep the code modular and testable.

## Submitting a Pull Request

1.  **Create a Branch**: Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature/my-new-feature
    ```
2.  **Commit Changes**: Make your changes and commit them with descriptive messages.
3.  **Push**: Push your branch to your fork.
    ```bash
    git push origin feature/my-new-feature
    ```
4.  **Open a PR**: Go to the original repository and open a Pull Request. Describe your changes and link to any relevant issues.

## Reporting Issues

If you find a bug or have a feature request, please open an issue in the repository with details about the problem or suggestion.
