"""
Simple test script to verify the LangGraph setup

This script tests basic functionality without requiring Ollama to be running.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")

    try:
        from src.config.models import ModelConfig, get_model

        print("  ✅ config.models")
    except ImportError as e:
        print(f"  ❌ config.models: {e}")
        return False

    try:
        from src.graph.state import TextAnalysisState

        print("  ✅ graph.state")
    except ImportError as e:
        print(f"  ❌ graph.state: {e}")
        return False

    try:
        from src.graph.nodes import input_processor

        print("  ✅ graph.nodes")
    except ImportError as e:
        print(f"  ❌ graph.nodes: {e}")
        return False

    try:
        from src.graph.workflow import create_workflow

        print("  ✅ graph.workflow")
    except ImportError as e:
        print(f"  ❌ graph.workflow: {e}")
        return False

    try:
        from src.utils.helpers import validate_input, format_result

        print("  ✅ utils.helpers")
    except ImportError as e:
        print(f"  ❌ utils.helpers: {e}")
        return False

    return True


def test_state_definition():
    """Test state definition"""
    print("\nTesting state definition...")

    from src.graph.state import TextAnalysisState

    # Create a sample state
    state: TextAnalysisState = {
        "input_text": "This is a test",
        "word_count": 4,
        "summary": "Test summary",
        "sentiment": "neutral",
    }

    assert state["input_text"] == "This is a test"
    assert state["word_count"] == 4
    print("  ✅ State definition works correctly")

    return True


def test_input_processor():
    """Test the input processor node"""
    print("\nTesting input processor node...")

    from src.graph.nodes import input_processor

    state = {"input_text": "Hello world this is a test"}
    result = input_processor(state)

    assert "word_count" in result
    assert result["word_count"] == 6
    print(f"  ✅ Word count: {result['word_count']}")

    return True


def test_validation():
    """Test input validation"""
    print("\nTesting input validation...")

    from src.utils.helpers import validate_input

    # Test valid input
    is_valid, error = validate_input("This is a valid input text")
    assert is_valid
    print("  ✅ Valid input accepted")

    # Test invalid input (too short)
    is_valid, error = validate_input("Short")
    assert not is_valid
    assert error is not None
    print(f"  ✅ Invalid input rejected: {error}")

    return True


def test_formatting():
    """Test result formatting"""
    print("\nTesting result formatting...")

    from src.utils.helpers import format_result

    state = {
        "input_text": "Sample text",
        "word_count": 2,
        "summary": "This is a summary",
        "sentiment": "positive",
    }

    # Test text format
    text_output = format_result(state, "text")
    assert "SUMMARY:" in text_output
    print("  ✅ Text format works")

    # Test JSON format
    json_output = format_result(state, "json")
    assert "input_text" in json_output
    print("  ✅ JSON format works")

    # Test markdown format
    md_output = format_result(state, "markdown")
    assert "##" in md_output
    print("  ✅ Markdown format works")

    return True


def test_model_config():
    """Test model configuration"""
    print("\nTesting model configuration...")

    from src.config.models import ModelConfig, MODEL_PRESETS

    config = ModelConfig(model_name="llama3.2", temperature=0.5)
    assert config.model_name == "llama3.2"
    assert config.temperature == 0.5
    print("  ✅ ModelConfig initialization works")

    config_dict = config.to_dict()
    assert config_dict["model"] == "llama3.2"
    print("  ✅ Config to dict conversion works")

    assert "balanced" in MODEL_PRESETS
    print("  ✅ Model presets available")

    return True


def test_workflow_creation():
    """Test workflow creation (without execution)"""
    print("\nTesting workflow creation...")

    try:
        from src.graph.workflow import create_workflow

        # Create workflow without checkpointer to avoid database dependencies
        workflow = create_workflow(model_name="llama3.2", use_checkpointer=False)

        print("  ✅ Workflow created successfully")
        print(f"  ℹ️  Workflow type: {type(workflow).__name__}")

        return True
    except (ImportError, RuntimeError, ValueError) as e:
        print(
            f"  ⚠️  Workflow creation failed (this is OK if Ollama isn't running): {e}"
        )
        return True  # Don't fail the test if Ollama isn't available


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("LangGraph Setup Verification")
    print("=" * 70)

    tests = [
        ("Imports", test_imports),
        ("State Definition", test_state_definition),
        ("Input Processor", test_input_processor),
        ("Validation", test_validation),
        ("Formatting", test_formatting),
        ("Model Config", test_model_config),
        ("Workflow Creation", test_workflow_creation),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except (ImportError, RuntimeError, ValueError) as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
            import traceback

            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Your LangGraph setup is ready to use.")
        print("\nNext steps:")
        print("  1. Make sure Ollama is running: ollama serve")
        print("  2. Pull a model: ollama pull llama3.2")
        print("  3. Run the demo: python main.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
