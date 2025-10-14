#!/bin/bash
# Helper script to run E2E tests
# Automatically starts server, runs tests, and cleans up
# Usage: ./scripts/run_e2e_tests.sh [--headed] [--browser <chromium|firefox|webkit>]

set -e

SOURCE_DIR="${SOURCE_DIR:-src}"
SERVER_PID=""
SERVER_STARTED_BY_SCRIPT=false

# Cleanup function to stop the server
cleanup() {
    if [ "$SERVER_STARTED_BY_SCRIPT" = true ] && [ -n "$SERVER_PID" ]; then
        echo ""
        echo "Stopping server (PID: $SERVER_PID)..."
        kill $SERVER_PID 2>/dev/null || true
        wait $SERVER_PID 2>/dev/null || true
        echo "Server stopped."
    fi
}

# Register cleanup function to run on script exit
trap cleanup EXIT INT TERM

# Check if server is already running
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "Server is already running on http://localhost:8000"
    echo "Using existing server for tests..."
else
    echo "Starting server on http://localhost:8000..."
    # Start server in background, redirect output to log file
    uvicorn ${SOURCE_DIR}.main:app --host 0.0.0.0 --port 8000 > /tmp/uvicorn_e2e.log 2>&1 &
    SERVER_PID=$!
    SERVER_STARTED_BY_SCRIPT=true
    
    echo "Server started (PID: $SERVER_PID), waiting for it to be ready..."
    
    # Wait up to 10 seconds for server to start
    for i in {1..20}; do
        if curl -s http://localhost:8000 > /dev/null 2>&1; then
            echo "Server is ready!"
            break
        fi
        if [ $i -eq 20 ]; then
            echo "ERROR: Server failed to start within 10 seconds"
            echo "Check /tmp/uvicorn_e2e.log for details"
            exit 1
        fi
        sleep 0.5
    done
fi

echo ""
echo "Running E2E tests..."
echo ""

# Pass all arguments to pytest and capture exit code
set +e
pytest -m e2e "$@"
TEST_EXIT_CODE=$?
set -e

# cleanup() will run automatically due to trap
exit $TEST_EXIT_CODE
