"""
Workflow definition and graph construction

This module defines the LangGraph workflow by connecting nodes
with edges and compiling the graph with necessary features like
checkpointing.
"""

import logging
from typing import Optional
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import TextAnalysisState
from .nodes import input_processor, create_summarizer_node

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_workflow(model_name: Optional[str] = None, use_checkpointer: bool = True):
    """
    Create and compile the LangGraph workflow

    This function builds the complete graph with:
    - State definition
    - Node definitions
    - Edge connections
    - Checkpointer for memory persistence

    The workflow follows this structure:
    START -> input_processor -> summarizer -> END

    Args:
        model_name: Name of the Ollama model to use (defaults to llama3.2)
        use_checkpointer: Whether to enable memory persistence

    Returns:
        Compiled LangGraph workflow ready for execution

    Example:
        >>> workflow = create_workflow()
        >>> result = workflow.invoke({"input_text": "Sample text..."})
    """
    logger.info("=" * 70)
    logger.info("Building LangGraph Workflow")
    logger.info("=" * 70)

    # Use default model if not specified
    if model_name is None:
        model_name = "llama3.2"

    logger.info(f"Model: {model_name}")
    logger.info(f"Checkpointer: {'Enabled' if use_checkpointer else 'Disabled'}")

    # Initialize the graph with our state schema
    logger.info("Initializing StateGraph with TextAnalysisState schema")
    builder = StateGraph(TextAnalysisState)

    # Add nodes to the graph
    logger.info("Adding nodes:")
    logger.info("  - input_processor: Calculates word count from input text")
    builder.add_node("input_processor", input_processor)

    logger.info(f"  - summarizer: Generates summary and sentiment using {model_name}")
    summarizer_node = create_summarizer_node(model_name=model_name)
    builder.add_node("summarizer", summarizer_node)

    # Define the edges (control flow)
    logger.info("Defining edges:")
    logger.info("  START -> input_processor")
    builder.add_edge(START, "input_processor")

    logger.info("  input_processor -> summarizer")
    builder.add_edge("input_processor", "summarizer")

    logger.info("  summarizer -> END")
    builder.add_edge("summarizer", END)

    # Compile the graph with optional checkpointer
    if use_checkpointer:
        logger.info("Compiling graph with MemorySaver checkpointer for persistence")
        checkpointer = MemorySaver()
        graph = builder.compile(checkpointer=checkpointer)
    else:
        logger.info("Compiling graph without checkpointer")
        graph = builder.compile()

    logger.info("=" * 70)
    logger.info("Workflow created successfully!")
    logger.info("=" * 70)

    return graph


def run_workflow(
    input_text: str, model_name: Optional[str] = None, thread_id: Optional[str] = None
) -> TextAnalysisState:
    """
    Convenience function to create and run the workflow

    This function handles the complete workflow execution:
    1. Creates the workflow
    2. Invokes it with the input text
    3. Returns the final state

    Args:
        input_text: The text to analyze
        model_name: Name of the Ollama model to use
        thread_id: Optional thread ID for persistent conversations

    Returns:
        Final state with all fields populated

    Example:
        >>> result = run_workflow("Your text here...")
        >>> print(result["summary"])
        >>> print(result["sentiment"])
    """
    logger.info("=" * 70)
    logger.info("Running Workflow")
    logger.info("=" * 70)
    logger.info(f"Input text length: {len(input_text)} characters")

    # Create the workflow - disable checkpointer if no thread_id provided
    use_checkpointer = thread_id is not None
    workflow = create_workflow(model_name=model_name, use_checkpointer=use_checkpointer)

    # Prepare config if thread_id is provided
    config = {}
    if thread_id:
        config = {"configurable": {"thread_id": thread_id}}
        logger.info("Using thread_id: %s", thread_id)
    else:
        logger.info("No thread_id provided - running without checkpointer")

    # Invoke the workflow
    logger.info("Invoking workflow...")
    result = workflow.invoke({"input_text": input_text}, config=config)

    logger.info("=" * 70)
    logger.info("Workflow completed successfully!")
    logger.info("=" * 70)

    return result


def stream_workflow(
    input_text: str, model_name: Optional[str] = None, thread_id: Optional[str] = None
):
    """
    Stream workflow execution for real-time updates

    This function streams the workflow execution, yielding
    updates as each node completes.

    Args:
        input_text: The text to analyze
        model_name: Name of the Ollama model to use
        thread_id: Optional thread ID for persistent conversations

    Yields:
        State updates from each node

    Example:
        >>> for update in stream_workflow("Your text here..."):
        ...     print(update)
    """
    logger.info("=" * 70)
    logger.info("Streaming Workflow")
    logger.info("=" * 70)

    # Create the workflow - disable checkpointer if no thread_id provided
    use_checkpointer = thread_id is not None
    workflow = create_workflow(model_name=model_name, use_checkpointer=use_checkpointer)

    # Prepare config
    config = {}
    if thread_id:
        config = {"configurable": {"thread_id": thread_id}}
        logger.info("Using thread_id: %s", thread_id)

    # Stream the workflow
    logger.info("Starting stream...")
    for update in workflow.stream(
        {"input_text": input_text}, config=config, stream_mode="updates"
    ):
        yield update

    logger.info("=" * 70)
    logger.info("Stream completed!")
    logger.info("=" * 70)
