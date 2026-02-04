# Contributing to Cribl Pipeline Visualizer

We welcome contributions! Please follow these guidelines to ensure a smooth process.

## Workflow

1.  **Fork** the repository.
2.  **Clone** your fork locally.
3.  **Create a Branch** for your feature or bugfix:
    ```bash
    git checkout -b feature/my-new-feature
    ```
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Make Changes**: Write your code and improve documentation.
6.  **Run Tests**: Ensure all tests pass.
    ```bash
    python -m unittest discover tests
    ```
7.  **Commit** your changes with a descriptive message.
8.  **Push** to your fork.
9.  **Submit a Pull Request**.

## Testing

*   We use `unittest`.
*   Run all tests: `python -m unittest discover tests`.
*   Ensure you add tests for any new features.
*   Note: `tests/test_app.py` has been removed. Tests are now consolidated in `tests/test_graph_generator.py` and `tests/test_cribl_api.py`.

## Code Style

*   Follow PEP 8 guidelines.
*   Document new code with docstrings.
