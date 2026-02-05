# Contributing to Cribl Pipeline Visualizer

Thank you for your interest in contributing to the Cribl Pipeline Visualizer! We welcome bug reports, feature requests, and pull requests.

## How to Contribute

1.  **Fork the repository** to your own GitHub account.
2.  **Clone the repository** to your local machine.
3.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b my-new-feature
    ```
4.  **Make your changes**. Ensure your code is clean and documented.
5.  **Run tests** to ensure you haven't broken anything:
    ```bash
    python -m unittest discover tests
    ```
6.  **Commit your changes** with a descriptive commit message.
7.  **Push your branch** to your fork:
    ```bash
    git push origin my-new-feature
    ```
8.  **Submit a Pull Request** to the main repository.

## Development Environment

1.  Create a `.env` file from `.env.example`.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Ensure `graphviz` is installed on your system.

## Testing

We use `unittest` for testing. Please ensure all existing tests pass and add new tests for any new features.

```bash
python -m unittest discover tests
```

## Code Style

*   Follow PEP 8 guidelines.
*   Write docstrings for all functions and classes.
*   Keep code simple and readable.
