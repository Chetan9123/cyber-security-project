#!/bin/bash

echo "Installing dependencies..."
pip install -r Requirment.txt

echo "Running FastAPI backend server..."
uvicorn app:app --reload --host 0.0.0.0 --port 8000
