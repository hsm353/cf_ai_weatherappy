#!/bin/bash

echo "========================================"
echo "Weather Chat Assistant - Local Server"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "Starting server..."
echo ""
echo "Visit: http://localhost:8787"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
