# To-Do list app

A simple RESTful API built with FastAPI, SQLAlchemy and PostgreSQL.

## How to run

1. Navigate to the project root
1. Create `.env` file: `cp backend/.env.example backend/.env`
1. Create and run the app containers: `docker compose up -d`
1. Interactive documentation of the endpoints is available at `localhost:8000/docs`

## Tests

1. Navigate to the project root
1. Create and run the app containers: `docker compose up -d`
1. Run all the tests: `docker exec -t todo_backend pytest tests`
1. Run all the tests and get a coverage report: `docker exec -t todo_backend pytest --cov=todo --cov-report=term-missing:skip-covered --cov-branch --cov-report=html tests`

## Development

### Pre-commit hooks

1. Install [pre-commit](https://pypi.org/project/pre-commit/): `pipx install pre-commit`
1. Navigate to project root
1. Set up git hook scripts: `pre-commit install`
1. (optional) Run against all enlighten files: `pre-commit run --all-files`