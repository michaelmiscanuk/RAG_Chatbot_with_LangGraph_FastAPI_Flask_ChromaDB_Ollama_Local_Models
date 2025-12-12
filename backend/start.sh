#!/bin/bash
set -e

# Decompress ChromaDB if needed
echo "Checking for ChromaDB compressed files..."
python3 ../decompress_files.py

# Use the PORT environment variable provided by Railway, or default to 8000
PORT="${PORT:-8000}"

echo "Starting uvicorn on port $PORT"

# Start uvicorn
exec uvicorn api:app --host 0.0.0.0 --port "$PORT" --log-level info
