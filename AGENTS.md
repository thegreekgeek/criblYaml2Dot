# AGENTS DOCUMENT
## objective
The task is to create a python program that will live in /opt/cribl, and look in ./default and ./local and find every yaml node in inputs.yml and outputs.yml that has disabled: false, and contains a connections section that defines a pipeline and the output node. Then once all the enabled nodes are gone through it generates a left to right graphviz dot file that details all these connections.

## Tooling
Python is the programming language used in this project, with additional libraries used as needed, like os and others.
