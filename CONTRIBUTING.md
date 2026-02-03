# Contributing to Cribl Pipeline Visualizer

Thank you for your interest in contributing to the Cribl Pipeline Visualizer! We welcome contributions that help improve the project.

## How to Contribute

1.  **Fork the Repository**: Create a fork of this repository to your own GitHub account.
2.  **Clone the Repository**: Clone your fork to your local machine.
    ```bash
    git clone https://github.com/your-username/cribl-viz.git
    cd cribl-viz
    ```
3.  **Create a Branch**: Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature/my-new-feature
    ```
4.  **Make Changes**: Implement your changes. Ensure you follow the project's coding standards.
5.  **Run Tests**: Run the existing tests and add new tests for your changes.
    ```bash
    python -m unittest discover tests
    ```
6.  **Commit Changes**: Commit your changes with a clear and descriptive commit message.
    ```bash
    git commit -m "Add a new feature to visualize X"
    ```
7.  **Push to Fork**: Push your branch to your fork.
    ```bash
    git push origin feature/my-new-feature
    ```
8.  **Submit a Pull Request**: Open a Pull Request (PR) from your fork to the main repository. Provide a detailed description of your changes.

## Coding Standards

*   **Python**: We use Python 3.9+. Please follow PEP 8 guidelines.
*   **Documentation**: Ensure all new functions and classes have docstrings. Update `README.md` and `AGENTS.md` if necessary.
*   **Formatting**: Use `black` or `flake8` if available to ensure code consistency.

## Testing

*   We use the `unittest` framework.
*   All new features must include corresponding unit tests.
*   Ensure all tests pass before submitting your PR.

## Reporting Issues

If you find a bug or have a feature request, please open an issue in the repository. Provide as much detail as possible, including steps to reproduce the issue.
