#!/usr/bin/env bash

docker compose up -d

if [ "$1" = "cov" ]; then
    docker exec -t todo_backend pytest --cov=todo --cov-report=term-missing:skip-covered --cov-branch --cov-report=html tests
else
    docker exec -t todo_backend pytest tests
fi
