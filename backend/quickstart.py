"""
Quick start script - run this to test the setup quickly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("\n" + "=" * 70)
print("LangGraph Quick Start")
print("=" * 70)

print("\n📋 Checking setup...\n")

# Check if required packages are installed
try:
    import langgraph  # type: ignore  # noqa: F401

    print("✅ langgraph installed")
except ImportError:
    print("❌ langgraph not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import langchain_ollama  # type: ignore  # noqa: F401

    print("✅ langchain-ollama installed")
except ImportError:
    print("❌ langchain-ollama not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

# Check if modules load correctly
try:
    from src.graph.workflow import create_workflow  # noqa: F401

    print("✅ Workflow module loads correctly")
except (ImportError, ModuleNotFoundError) as e:
    print(f"❌ Error loading workflow: {e}")
    sys.exit(1)

# Check Ollama connection (optional)
print("\n🔌 Checking Ollama connection...")
try:
    from langchain_ollama import ChatOllama  # type: ignore

    model = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    # Try a simple call
    response = model.invoke("Say 'OK' if you can read this.")
    print("✅ Ollama is running and responding")
    print(f"   Response: {response.content[:50]}...")
except (ConnectionError, TimeoutError, ValueError) as e:
    print("⚠️  Ollama connection failed (make sure it's running)")
    print(f"   Error: {str(e)[:100]}")
    print("\n   To start Ollama:")
    print("   1. Run: ollama serve")
    print("   2. Run: ollama pull llama3.2")

print("\n" + "=" * 70)
print("Setup Status")
print("=" * 70)

print("\n✅ Your LangGraph project is set up correctly!")
print("\n📚 Next steps:")
print("   1. Run the demo:     python main.py")
print("   2. Test setup:       python test_setup.py")
print("   3. See examples:     cd examples && python examples.py")
print("   4. Use CLI:          python main.py --sample 0")
print("\n💡 Tips:")
print("   - Use --help to see all CLI options")
print("   - Check README.md for detailed documentation")
print("   - Explore examples/ folder for code samples")

print("\n" + "=" * 70)
