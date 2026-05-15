# SYGA(See Your Graph Algorithm) Engine

The engine which runs algorithms and computes frames.

## How to run 

### Locally

1. Make sure your version of Python is at least 3.11
2. Run `pip install -r requirements.txt`
3. Run `python3 src/main.py`. Now the engine endpoint should be exposed through `http://localhost:5000`.

Running the code is as simple as sending a POST request to the endpoint with a JSON body with a field named `code`. In this field, just add your SYGA code!

### Dockerhub

A production image of the webapp can be downloaded from [Dockerhub](https://hub.docker.com/repository/docker/kheltan/syga-prod-engine).

## Legacy issues

Huge thanks to Milan Wikarski for starting this project and putting in an incredible amount of work before I took over.

The project was written a while ago so there are some things missing from a modern Python repository. For instance, typehints. Every change has to be made without breaking the production instance so it will be a while before this is fixed!

