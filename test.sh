#!/usr/bin/env bash

# Cleanup if containers are started by this script
top_output=$(docker compose top)

cleanup() {
    if [ -z "$top_output" ]; then 
        docker compose down
    fi
}

trap cleanup EXIT

# Run tests
docker compose up -d

if [ "$1" = "cov" ]; then
    docker exec -t todo_backend pytest --cov=todo --cov-report=term-missing:skip-covered --cov-branch --cov-report=html tests
else
    docker exec -t todo_backend pytest tests
fi
