#!/usr/bin/env bash

# Script args
PYTEST_ARGS=""
while getopts ":c" opt; do
    case $opt in
        c)
            PYTEST_ARGS="--cov=todo --cov-report=term-missing:skip-covered --cov-branch --cov-report=html"
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            exit 1
            ;;
    esac
done

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
docker exec -t todo_backend pytest $PYTEST_ARGS tests
