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
from langchain_core.messages import HumanMessage

from .state import ChatState
from .nodes import retrieve, generate

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_workflow(use_checkpointer: bool = True):
    """
    Create and compile the Chatbot workflow

    This function builds the complete graph with:
    - State definition
    - Node definitions
    - Edge connections
    - Checkpointer for memory persistence

    The workflow follows this structure:
    START -> retrieve -> generate -> END
    """
    logger.info("=" * 70)
    logger.info("Building Chatbot Workflow")
    logger.info("=" * 70)

    # Initialize the graph with our state schema
    builder = StateGraph(ChatState)

    # Add nodes to the graph
    builder.add_node("retrieve", retrieve)
    builder.add_node("generate", generate)

    # Define the edges (control flow)
    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)

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


def run_workflow(input_text: str, thread_id: Optional[str] = None) -> ChatState:
    """
    Convenience function to create and run the workflow
    """
    logger.info("=" * 70)
    logger.info("Running Workflow")
    logger.info("=" * 70)

    # Create the workflow
    use_checkpointer = thread_id is not None
    workflow = create_workflow(use_checkpointer=use_checkpointer)

    # Prepare config if thread_id is provided
    config = {}
    if thread_id:
        config = {"configurable": {"thread_id": thread_id}}
        logger.info("Using thread_id: %s", thread_id)

    # Invoke the workflow
    logger.info("Invoking workflow...")
    result = workflow.invoke(
        {"messages": [HumanMessage(content=input_text)]}, config=config
    )

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
