"""
State definition for the LangGraph workflow

This module defines the state schema that will be shared across
all nodes in the graph. The state persists throughout execution
and nodes can read from and write to it.
"""

from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    """
    State schema for the chatbot workflow

    - messages: Conversation history (list of messages)
    - context: Retrieved documents from ChromaDB
    """

    messages: Annotated[List[BaseMessage], add_messages]
    context: List[str]
