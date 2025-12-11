"""
Main entry point for the LangGraph Text Analysis Backend

This module provides the main entry point for running the FastAPI server.
"""

import uvicorn
import os
from pathlib import Path

# Add the parent directory to the path so we can import api
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from api import app


def main():
    """
    Main entry point for running the FastAPI application
    """
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"Starting Text Analysis API server on {host}:{port}")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")

    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=os.environ.get("RELOAD", "false").lower() == "true",
        log_level=os.environ.get("LOG_LEVEL", "info"),
    )


if __name__ == "__main__":
    main()
