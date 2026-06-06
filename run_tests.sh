#!/bin/bash

echo "===================================================="
echo "🚀 Starting Quantium Automated CI Test Suite Wrapper"
echo "===================================================="

# 1. Determine script directory path context to make it machine-independent
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 2. Check for the local virtual environment folder layout
if [ -d ".venv" ]; then
    echo "📦 Virtual environment found. Activating..."
    # On Git Bash / Linux / macOS, use the standard POSIX activation path
    source .venv/bin/activate
else
    echo "❌ Error: Virtual environment (.venv) directory missing."
    exit 1
fi

# 3. Execute the test suite framework using Pytest
echo "🧪 Running unit testing module assertions..."
pytest test_app.py
TEST_RESULT=$?

# 4. Process the system exit states dynamically
echo "===================================================="
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ SUCCESS: All test assertions passed flawlessly!"
    echo "===================================================="
    exit 0
else
    echo "💥 FAILURE: Test suite failed with exit code $TEST_RESULT."
    echo "===================================================="
    exit 1
fi