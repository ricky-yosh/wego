#!/bin/bash
echo "Creating the virtual environment..."
python3 -m venv virtual-env
echo "Activating the virtual environment..."
source virtual-env/bin/activate
echo "Note: Virtual environment only runs during the duration of this script.
If you want to run it manually do: source virtual-env/bin/activate"

echo "Installing required Python packages..."
pip install -r requirements.txt

echo "Running tests..."
pytest