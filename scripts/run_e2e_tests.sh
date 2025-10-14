#!/bin/bash
# Helper script to run E2E tests
# Usage: ./scripts/run_e2e_tests.sh [--headed] [--browser <chromium|firefox|webkit>]

set -e

SOURCE_DIR="${SOURCE_DIR:-src}"

# Check if server is already running
if ! curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "Server is not running on http://localhost:8000"
    echo "Please start the server first:"
    echo "  # Example for FastAPI:"
    echo "  uvicorn ${SOURCE_DIR}.main:app --host 0.0.0.0 --port 8000"
    echo ""
    echo "  # Example for Flask:"
    echo "  flask run --host 0.0.0.0 --port 8000"
    exit 1
fi

echo "Server is running on http://localhost:8000"
echo "Running E2E tests..."
echo ""

# Pass all arguments to pytest
pytest -m e2e "$@"
