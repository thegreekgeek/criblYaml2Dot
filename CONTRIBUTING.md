# Contributing to Cribl Pipeline Visualizer

Thank you for your interest in contributing to the Cribl Pipeline Visualizer!

## Getting Started

1.  **Fork the repository**: Click the "Fork" button on the top right of the repository page.
2.  **Clone your fork**:
    ```bash
    git clone https://github.com/your-username/cribl-pipeline-visualizer.git
    cd cribl-pipeline-visualizer
    ```
3.  **Set up your environment**:
    - Install Python 3.9+.
    - Install Graphviz system package.
    - Create a virtual environment and install dependencies:
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install -r requirements.txt
      ```
    - Create a `.env` file from `.env.example`.

## Development Workflow

1.  **Create a branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
2.  **Make your changes**: Write clean, documented code.
3.  **Run tests**: Ensure all tests pass.
    ```bash
    python -m unittest discover tests
    ```
4.  **Commit your changes**:
    ```bash
    git add .
    git commit -m "Description of your changes"
    ```
5.  **Push to your fork**:
    ```bash
    git push origin feature/your-feature-name
    ```
6.  **Create a Pull Request**: Go to the original repository and create a Pull Request from your fork.

## Testing

We use `unittest` for testing. Please ensure you add tests for any new features or bug fixes.

To run tests:
```bash
python -m unittest discover tests
```

## Code Style

- Follow PEP 8 guidelines.
- Add docstrings to all functions and classes.
- Update `docs/CODE_REFERENCE.md` if you change the API or internal logic.
