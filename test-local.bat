@echo off
REM test-local.bat - Script to run tests locally on Windows

echo Installing test dependencies...
pip install -r requirements-test.txt

echo Running tests...
python -m pytest test_app.py -v --cov=app

echo Tests completed!
pause