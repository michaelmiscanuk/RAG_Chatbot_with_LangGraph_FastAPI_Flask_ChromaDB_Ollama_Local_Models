"""
Model configuration and initialization

This module provides a centralized way to configure and initialize
Ollama models with different parameters.
"""

# pylint: disable=import-error

import os
from typing import Optional
from langchain_ollama import ChatOllama


class MockChatOllama:
    """Mock ChatOllama for testing without Ollama"""

    def invoke(self, messages):
        # Mock responses based on the prompt
        prompt = messages[1].content if len(messages) > 1 else ""
        if "Summarize" in prompt:
            return type(
                "Response",
                (),
                {
                    "content": "This is a mock summary of the provided text. It captures the main points and provides a concise overview."
                },
            )()
        elif "sentiment" in prompt.lower():
            return type("Response", (), {"content": "neutral"})()
        else:
            return type("Response", (), {"content": "Mock response"})()


class ModelConfig:
    """Configuration class for Ollama models"""

    def __init__(
        self,
        model_name: str = "llama3.2",
        temperature: float = 0.7,
        base_url: Optional[str] = None,
        num_ctx: int = 2048,
        top_p: float = 0.9,
        top_k: int = 40,
    ):
        """
        Initialize model configuration

        Args:
            model_name: Name of the Ollama model to use
            temperature: Sampling temperature (0.0 to 1.0)
            base_url: Base URL for Ollama API (defaults to localhost)
            num_ctx: Context window size
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
        """
        self.model_name = model_name
        self.temperature = temperature
        # Use OLLAMA_HOST from Railway environment, fallback to localhost for dev
        self.base_url = base_url or os.getenv(
            "OLLAMA_HOST", os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        self.num_ctx = num_ctx
        self.top_p = top_p
        self.top_k = top_k

    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            "model": self.model_name,
            "temperature": self.temperature,
            "base_url": self.base_url,
            "num_ctx": self.num_ctx,
            "top_p": self.top_p,
            "top_k": self.top_k,
        }


def get_model(
    model_name: Optional[str] = None, temperature: float = 0.7, **kwargs
) -> ChatOllama:
    """
    Get a configured ChatOllama instance

    This is the main function to get a model instance. It supports
    passing a model name and configuration parameters.

    Args:
        model_name: Name of the Ollama model (defaults to env var or llama3.2)
        temperature: Sampling temperature
        **kwargs: Additional parameters for ModelConfig

    Returns:
        Configured ChatOllama instance

    Example:
        >>> model = get_model("llama3.2", temperature=0.5)
        >>> model = get_model()  # Uses default configuration
    """
    if model_name is None:
        model_name = os.getenv("DEFAULT_MODEL", "llama3.2")

    config = ModelConfig(model_name=model_name, temperature=temperature, **kwargs)

    # Try to use Ollama, but fall back to mock if not available
    try:
        model = ChatOllama(
            model=config.model_name,
            temperature=config.temperature,
            base_url=config.base_url,
            num_ctx=config.num_ctx,
            # Additional Ollama-specific parameters
            format="",  # Empty string for regular text generation
        )
        # Test if Ollama is running by trying a simple invoke
        model.invoke([{"role": "user", "content": "test"}])
        return model
    except Exception as e:
        print(f"Ollama not available, using mock model. Error: {str(e)}")
        return MockChatOllama()


# Predefined model configurations for different use cases
MODEL_PRESETS = {
    "creative": ModelConfig(
        model_name="llama3.2",
        temperature=0.9,
        top_p=0.95,
    ),
    "balanced": ModelConfig(
        model_name="llama3.2",
        temperature=0.7,
        top_p=0.9,
    ),
    "precise": ModelConfig(
        model_name="llama3.2",
        temperature=0.3,
        top_p=0.8,
    ),
    "deterministic": ModelConfig(
        model_name="llama3.2",
        temperature=0.0,
        top_p=1.0,
    ),
}


def get_model_from_preset(preset_name: str = "balanced") -> ChatOllama:
    """
    Get a model using a predefined preset configuration

    Args:
        preset_name: Name of the preset ('creative', 'balanced', 'precise', 'deterministic')

    Returns:
        Configured ChatOllama instance

    Example:
        >>> model = get_model_from_preset("creative")
    """
    if preset_name not in MODEL_PRESETS:
        raise ValueError(
            f"Unknown preset: {preset_name}. "
            f"Available presets: {list(MODEL_PRESETS.keys())}"
        )

    config = MODEL_PRESETS[preset_name]
    return ChatOllama(
        model=config.model_name,
        temperature=config.temperature,
        base_url=config.base_url,
        num_ctx=config.num_ctx,
        format="",
    )
