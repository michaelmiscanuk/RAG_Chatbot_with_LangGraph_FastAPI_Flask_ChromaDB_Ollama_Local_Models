"""
Node implementations for the LangGraph workflow

This module contains the node functions that perform the actual
processing in the workflow. Each node receives the current state
and returns updates to it.
"""

import logging
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage

from .state import TextAnalysisState
from ..config.models import get_model

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def input_processor(state: TextAnalysisState) -> Dict[str, Any]:
    """
    First node: Process input text and calculate word count

    This node reads the input_text from state and calculates
    the word count, which it returns as a state update.

    Args:
        state: Current state containing input_text

    Returns:
        Dictionary with word_count update
    """
    logger.info("=" * 60)
    logger.info("NODE 1: Input Processor - Starting")
    logger.info("=" * 60)

    input_text = state.get("input_text", "")

    if not input_text:
        logger.warning("No input text provided")
        return {"word_count": 0}

    # Calculate word count
    words = input_text.split()
    word_count = len(words)

    logger.info(f"Input text length: {len(input_text)} characters")
    logger.info(f"Word count calculated: {word_count} words")
    logger.info(f"First 100 characters: {input_text[:100]}...")

    logger.info("=" * 60)
    logger.info("NODE 1: Input Processor - Completed")
    logger.info("=" * 60)

    return {"word_count": word_count}


def summarizer(
    state: TextAnalysisState, model_name: str = "llama3.2"
) -> Dict[str, Any]:
    """
    Second node: Generate summary and sentiment analysis

    This node reads the input_text and word_count from state,
    then uses an LLM to generate both a summary and sentiment
    analysis, returning both as state updates.

    Args:
        state: Current state containing input_text and word_count
        model_name: Name of the Ollama model to use

    Returns:
        Dictionary with summary and sentiment updates
    """
    logger.info("=" * 60)
    logger.info("NODE 2: Summarizer - Starting")
    logger.info("=" * 60)

    input_text = state.get("input_text", "")
    word_count = state.get("word_count", 0)

    logger.info(f"Processing text with {word_count} words")
    logger.info(f"Using model: {model_name}")

    if not input_text:
        logger.warning("No input text to summarize")
        return {"summary": "No text provided", "sentiment": "neutral"}

    try:
        # Get model instance
        logger.info("Initializing LLM model...")
        model = get_model(model_name=model_name, temperature=0.7)

        # Generate summary
        logger.info("Generating summary...")
        summary_prompt = f"""Summarize the following text in 2-3 sentences. Be concise and capture the main points.

Text ({word_count} words):
{input_text}

Summary:"""

        summary_messages = [
            SystemMessage(
                content="You are a helpful assistant that creates concise summaries."
            ),
            HumanMessage(content=summary_prompt),
        ]

        summary_response = model.invoke(summary_messages)
        summary = summary_response.content.strip()

        logger.info(f"Summary generated: {len(summary)} characters")
        logger.info(f"Summary preview: {summary[:100]}...")

        # Generate sentiment analysis
        logger.info("Analyzing sentiment...")
        sentiment_prompt = f"""Analyze the sentiment of the following text. 
Respond with ONLY ONE WORD from these options: positive, negative, neutral, or mixed.

Text:
{input_text}

Sentiment:"""

        sentiment_messages = [
            SystemMessage(
                content="You are a sentiment analysis assistant. Respond with only one word: positive, negative, neutral, or mixed."
            ),
            HumanMessage(content=sentiment_prompt),
        ]

        sentiment_response = model.invoke(sentiment_messages)
        sentiment = sentiment_response.content.strip().lower()

        # Validate sentiment response
        valid_sentiments = ["positive", "negative", "neutral", "mixed"]
        if sentiment not in valid_sentiments:
            logger.warning(f"Invalid sentiment '{sentiment}', defaulting to 'neutral'")
            sentiment = "neutral"

        logger.info(f"Sentiment detected: {sentiment}")

        logger.info("=" * 60)
        logger.info("NODE 2: Summarizer - Completed")
        logger.info("=" * 60)

        return {"summary": summary, "sentiment": sentiment}

    except (ValueError, TypeError, ConnectionError, TimeoutError) as e:
        logger.error("Error in summarizer node: %s", str(e), exc_info=True)
        return {"summary": f"Error generating summary: {str(e)}", "sentiment": "error"}


# Node function factories for dependency injection
def create_summarizer_node(model_name: str = "llama3.2"):
    """
    Create a summarizer node with a specific model

    This is a factory function that returns a node function
    configured with a specific model name.

    Args:
        model_name: Name of the Ollama model to use

    Returns:
        Node function configured with the model
    """

    def node(state: TextAnalysisState) -> Dict[str, Any]:
        return summarizer(state, model_name=model_name)

    return node
