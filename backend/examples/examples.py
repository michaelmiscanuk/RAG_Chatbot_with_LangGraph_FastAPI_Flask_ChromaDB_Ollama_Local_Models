"""
Example scripts demonstrating various usage patterns of the workflow
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.graph.workflow import create_workflow, run_workflow
from src.config.models import get_model_from_preset
from src.utils.helpers import print_result


def example_basic_usage():
    """Example 1: Basic usage with default settings"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 70)

    text = """
    Machine learning is a subset of artificial intelligence that enables 
    computers to learn and improve from experience without being explicitly 
    programmed. It has applications in various fields including healthcare, 
    finance, and autonomous vehicles.
    """

    result = run_workflow(input_text=text)
    print_result(result)


def example_custom_model():
    """Example 2: Using a different model"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Custom Model")
    print("=" * 70)

    text = """
    Climate change is one of the most pressing challenges facing humanity today.
    Rising temperatures, melting ice caps, and extreme weather events are 
    becoming more frequent and severe.
    """

    # You can specify any Ollama model you have installed
    result = run_workflow(input_text=text, model_name="llama3.2")
    print_result(result)


def example_with_persistence():
    """Example 3: Using thread persistence for conversations"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Persistent Conversations")
    print("=" * 70)

    workflow = create_workflow(model_name="llama3.2")

    # First invocation
    result1 = workflow.invoke(
        {"input_text": "Python is a versatile programming language."},
        {"configurable": {"thread_id": "conversation-1"}},
    )

    print("\nFirst analysis:")
    print_result(result1)

    # Second invocation with same thread_id
    # The workflow remembers previous state
    result2 = workflow.invoke(
        {"input_text": "JavaScript is widely used for web development."},
        {"configurable": {"thread_id": "conversation-1"}},
    )

    print("\nSecond analysis (same thread):")
    print_result(result2)


def example_streaming():
    """Example 4: Streaming workflow execution"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Streaming Execution")
    print("=" * 70)

    from src.graph.workflow import stream_workflow

    text = """
    Renewable energy sources like solar and wind power are becoming 
    increasingly cost-effective and efficient. Many countries are 
    transitioning away from fossil fuels to reduce carbon emissions.
    """

    print(f"\nInput: {text[:100]}...\n")
    print("Streaming updates:")

    for update in stream_workflow(input_text=text):
        print(f"\n📦 Node completed: {list(update.keys())}")
        for key, value in update.items():
            print(f"   {key}: {value}")


def example_model_presets():
    """Example 5: Using model presets"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Model Presets")
    print("=" * 70)

    # Available presets: 'creative', 'balanced', 'precise', 'deterministic'

    print("\n1. Using 'precise' preset (low temperature):")
    model = get_model_from_preset("precise")
    print(f"   Temperature: {model.temperature}")

    print("\n2. Using 'creative' preset (high temperature):")
    model = get_model_from_preset("creative")
    print(f"   Temperature: {model.temperature}")


def example_error_handling():
    """Example 6: Error handling"""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Error Handling")
    print("=" * 70)

    from src.utils.helpers import validate_input

    # Test with invalid input
    test_inputs = [
        ("", "Empty string"),
        ("Too short", "Too short text"),
        ("Valid text that is long enough to pass validation", "Valid text"),
    ]

    for text, description in test_inputs:
        is_valid, error = validate_input(text, min_length=10)
        print(f"\n{description}:")
        if is_valid:
            print("   ✅ Valid input")
        else:
            print(f"   ❌ Invalid: {error}")


def example_direct_node_usage():
    """Example 7: Using nodes directly"""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Direct Node Usage")
    print("=" * 70)

    from src.graph.nodes import input_processor, summarizer

    text = "Blockchain technology provides a decentralized and secure way to record transactions."

    # Create initial state
    state = {"input_text": text}

    print("\n1. Running input_processor node:")
    state.update(input_processor(state))
    print(f"   Word count: {state['word_count']}")

    print("\n2. Running summarizer node:")
    state.update(summarizer(state, model_name="llama3.2"))
    print(f"   Summary: {state['summary'][:100]}...")
    print(f"   Sentiment: {state['sentiment']}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("LangGraph Workflow Examples")
    print("=" * 70)

    examples = [
        ("1", "Basic Usage", example_basic_usage),
        ("2", "Custom Model", example_custom_model),
        ("3", "Persistent Conversations", example_with_persistence),
        ("4", "Streaming Execution", example_streaming),
        ("5", "Model Presets", example_model_presets),
        ("6", "Error Handling", example_error_handling),
        ("7", "Direct Node Usage", example_direct_node_usage),
    ]

    print("\nAvailable examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")

    print("\nRun all examples? (y/n): ", end="")
    choice = input().strip().lower()

    if choice == "y":
        for num, name, func in examples:
            try:
                func()
            except (ValueError, RuntimeError, ConnectionError) as e:
                print(f"\n❌ Error in example {num}: {str(e)}")
    else:
        print("\nTo run a specific example, call it directly in the code.")
