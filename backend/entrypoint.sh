#!/usr/bin/env bash

echo "Starting server..."
uvicorn todo.main:app --host 0.0.0.0 --port 8000 --reload
