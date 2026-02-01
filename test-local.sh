#!/bin/bash
# test-local.sh - Script to run tests locally

set -e

echo "Installing test dependencies..."
pip install -r requirements-test.txt

echo "Running tests..."
python -m pytest test_app.py -v --cov=app

echo "Tests completed!"