# To-Do list app

A simple RESTful API built with FastAPI, SQLAlchemy and PostgreSQL.

## Contents
* [How to run](#how-to-run)
* [Tests](#tests)
* [Development](#development)
    * [Pre-commit](#pre-commit-hooks)
    * [Local project environment](#local-project-environment)

## How to run

1. Navigate to the project root
1. Create `.env` file: `cp backend/.env.example backend/.env`
1. Create and run the app containers: `docker compose up -d`
1. Interactive documentation of the endpoints is available at `localhost:8000/docs`

## Tests

1. Navigate to the project root
1. Run all the tests: `bash test.sh`
1. Run all the tests and get a coverage report: `bash test.sh cov`

## Development

### Pre-commit hooks

1. Install [pre-commit](https://pypi.org/project/pre-commit/): `pipx install pre-commit`
1. Navigate to the project root
1. Set up git hook scripts: `pre-commit install`
1. (optional) Run against all files: `pre-commit run --all-files`

### Local project environment

1. Install the required Python version: `pyenv install 3.11`
1. Set the required Python version in the current terminal session: `pyenv shell 3.11`
1. Navigate to the `backend` directory
1. Create the env: `pyenv which python | xargs poetry env use`
1. Install the project dependencies: `poetry install`
