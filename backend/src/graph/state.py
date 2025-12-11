"""
State definition for the LangGraph workflow

This module defines the state schema that will be shared across
all nodes in the graph. The state persists throughout execution
and nodes can read from and write to it.
"""

from typing import TypedDict


class TextAnalysisState(TypedDict):
    """
    State schema for the text analysis workflow

    This state contains three distinct fields that are updated
    by different nodes in the workflow:

    - input_text: The original text provided by the user (set initially)
    - word_count: Number of words in the input (set by input_processor node)
    - summary: Generated summary of the text (set by summarizer node)
    - sentiment: Sentiment analysis result (set by summarizer node)
    """

    # Input field - provided by user
    input_text: str

    # Metadata field - set by input_processor node
    word_count: int

    # Output fields - set by summarizer node
    summary: str
    sentiment: str
