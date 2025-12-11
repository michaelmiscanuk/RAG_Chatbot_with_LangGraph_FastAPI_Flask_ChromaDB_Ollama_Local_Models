"""
Node implementations for the LangGraph workflow

This module contains the node functions that perform the actual
processing in the workflow. Each node receives the current state
and returns updates to it.
"""

import os
import logging
from typing import Dict, Any, List
from pathlib import Path
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from .state import ChatState
from ..config.models import get_model, get_langchain_azure_embedding_model

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent.parent / "data"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"


def retrieve(state: ChatState) -> Dict[str, Any]:
    """
    Retrieve relevant documents from ChromaDB based on the last user message.
    """
    logger.info("NODE: Retrieve - Starting")

    messages = state.get("messages", [])
    if not messages:
        logger.warning("No messages found in state")
        return {"context": []}

    last_message = messages[-1]
    query = last_message.content

    logger.info(f"Querying ChromaDB for: {query}")

    try:
        if not CHROMA_DB_DIR.exists():
            logger.warning(f"ChromaDB directory not found at {CHROMA_DB_DIR}")
            return {"context": []}

        embedding_model = get_langchain_azure_embedding_model()
        vectorstore = Chroma(
            persist_directory=str(CHROMA_DB_DIR), embedding_function=embedding_model
        )

        # Search for top 5 similar documents
        docs = vectorstore.similarity_search(query, k=5)
        context = [doc.page_content for doc in docs]

        logger.info(f"Retrieved {len(context)} documents")
        return {"context": context}

    except Exception as e:
        logger.error(f"Error in retrieve node: {e}")
        return {"context": []}


def generate(state: ChatState) -> Dict[str, Any]:
    """
    Generate a response using the LLM, context, and conversation history.
    """
    logger.info("NODE: Generate - Starting")

    messages = state.get("messages", [])
    context = state.get("context", [])

    # Format context
    context_str = "\n\n".join(context) if context else "No relevant information found."

    system_prompt = f"""You are a helpful customer support assistant. 
Use the following context to answer the user's question. 
If the answer is not in the context, politely say that you don't have the answer and suggest contacting human support at support@example.com.
Keep your answers concise and helpful.

Context:
{context_str}
"""

    # Prepare messages for LLM
    # We prepend the system prompt to the conversation history
    prompt_messages = [SystemMessage(content=system_prompt)] + messages

    try:
        model = get_model(temperature=0.7)
        response = model.invoke(prompt_messages)

        logger.info("Response generated")
        return {"messages": [response]}

    except Exception as e:
        logger.error(f"Error in generate node: {e}")
        return {
            "messages": [
                AIMessage(
                    content="I apologize, but I encountered an error while processing your request."
                )
            ]
        }
