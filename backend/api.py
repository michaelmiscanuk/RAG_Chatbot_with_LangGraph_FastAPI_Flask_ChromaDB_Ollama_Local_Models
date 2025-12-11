"""
FastAPI REST API for LangGraph Text Analysis Backend

This module provides REST API endpoints for the text analysis workflow.
Designed to be deployed on Render.com and accessed by the frontend.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# from src.graph.workflow import run_workflow  # Import later to avoid startup issues
# from src.utils.helpers import validate_input  # Import later to avoid startup issues

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Text Analysis API",
    description="LangGraph-powered text analysis with summary and sentiment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS - Allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",  # Local development
        "http://127.0.0.1:5000",
        "https://summarizer-agent-langgraph-ufot.vercel.app",  # Production Vercel frontend
        "https://*.vercel.app",  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Request/Response models
class TextAnalysisRequest(BaseModel):
    """Request model for text analysis"""

    text: str = Field(
        ..., min_length=1, max_length=10000, description="The text to analyze"
    )
    model_name: Optional[str] = Field(
        default="qwen2.5-coder:0.5b",
        description="Ollama model name to use for analysis",
    )


class TextAnalysisResponse(BaseModel):
    """Response model for text analysis"""

    input_text: str
    word_count: int
    character_count: int
    summary: str
    sentiment: str
    model_used: str
    success: bool = True


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    message: str


class ErrorResponse(BaseModel):
    """Error response model"""

    success: bool = False
    error: str
    detail: Optional[str] = None


# API Endpoints
@app.get("/")
async def root():
    """
    Root endpoint - API health check
    """
    return {
        "status": "healthy",
        "message": "Text Analysis API is running. Visit /docs for API documentation.",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy", "message": "API is operational"}


@app.post("/api/analyze")
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text and return summary with sentiment

    Args:
        request: TextAnalysisRequest with text and optional model_name

    Returns:
        TextAnalysisResponse with analysis results

    Raises:
        HTTPException: If validation or processing fails
    """
    try:
        logger.info("Received analysis request for %d characters", len(request.text))

        # Validate input
        from src.utils.helpers import validate_input

        is_valid, error_message = validate_input(request.text)
        if not is_valid:
            logger.warning("Invalid input: %s", error_message)
            raise HTTPException(status_code=400, detail=error_message)

        # Run workflow
        from src.graph.workflow import run_workflow

        logger.info("Running workflow with model: %s", request.model_name)
        result = run_workflow(
            input_text=request.text,
            model_name=request.model_name,
            thread_id=None,  # Each request is independent
        )

        # Prepare response
        response = {
            "input_text": result["input_text"],
            "word_count": result["word_count"],
            "character_count": len(request.text),
            "summary": result["summary"],
            "sentiment": result["sentiment"],
            "model_used": request.model_name,
            "success": True,
        }

        logger.info("Analysis completed successfully")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error processing request: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail="Internal server error: %s" % str(e)
        )


@app.get("/api/models")
async def list_models():
    """
    List available Ollama models

    Returns:
        List of available model names
    """
    # Default models that should be available
    # In production, you might want to query Ollama directly
    models = [
        "qwen2.5-coder:0.5b",
        "llama3.2",
        "llama3.2:1b",
        "llama3.2:3b",
        "mistral",
        "codellama",
    ]
    return {"models": models, "default": "qwen2.5-coder:0.5b"}


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "detail": str(exc),
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    logger.error("Internal server error: %s", str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again later.",
        },
    )


# Run with: uvicorn api:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn

    reload_mode = os.environ.get("RELOAD", "false").lower() == "true"
    uvicorn.run(
        "api:app", host="0.0.0.0", port=8000, reload=reload_mode, log_level="info"
    )
