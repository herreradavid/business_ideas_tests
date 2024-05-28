#!/usr/bin/env bash

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    # Create the virtual environment if it doesn't exist
    python3.11 -m venv venv
    echo "Virtual environment created."
fi

# Activate the virtual environment
source ./venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Environment setup complete"