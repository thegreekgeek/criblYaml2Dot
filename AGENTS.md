# AGENTS DOCUMENT

## objective
The task is to create a python program that will live in /opt/cribl, and look in ./default and ./local and find every yaml node in inputs.yml and outputs.yml that has disabled: false, and contains a connections section that defines a pipeline and the output node. Then once all the enabled nodes are gone through it generates a left to right graphviz dot file that details all these connections.

## Tooling
Python is the programming language used in this project, with additional libraries used as needed, like os and others.

## Project Goals
The eventual end goal is to turn this into a dockerized application that can be deployed to a observability cluster and visualize the logstream logic. This will involve
 - Retooling the app to use the cribl api instead file access to read the inputs and outputs and pipelines and whatnot.
    - creating a function to access the cribl api and retrieve the necessary data.
    - creating a function to generate the dot file from the retrieved data.
 - Creating a dockerfile to build the application into a docker image.
 - Creating a docker-compose file to deploy the application to a observability cluster.
 
 ## Additional Documentation
 Additional documentation can be found in this folder, the files (./cribl_api_intro.md)[Cribl API Introduction] and (./cribl_api_update_configs.md)[Cribl API Update Configs]
 
 Cribl Stream APIdocs are [./cribl-apidocs-4.15.1-1b453caa.yml](cribl-apidocs-4.15.1-1b453caa.yml)
 
 Api Authentication docs are available [./cribl_api_authentication.md](HERE)
