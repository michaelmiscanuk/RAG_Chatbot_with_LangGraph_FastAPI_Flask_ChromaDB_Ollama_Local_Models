"""
Quick start script - run this to test the setup quickly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("\n" + "=" * 70)
print("LangGraph Chatbot Quick Start")
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

try:
    import langchain_chroma  # type: ignore  # noqa: F401

    print("✅ langchain-chroma installed")
except ImportError:
    print("❌ langchain-chroma not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

# Check if modules load correctly
try:
    from src.graph.workflow import run_workflow  # noqa: F401

    print("✅ Workflow module loads correctly")
except (ImportError, ModuleNotFoundError) as e:
    print(f"❌ Error loading workflow: {e}")
    sys.exit(1)

# Check Ollama connection (optional)
print("\n🔌 Checking Ollama connection...")
try:
    from src.config.models import get_model

    model = get_model()
    # Try a simple call
    response = model.invoke("Say 'OK'")
    print("✅ Ollama is running and responding")
    print(f"   Response: {response.content}")
except Exception as e:
    print("⚠️  Ollama connection failed or using mock")
    print(f"   Error: {str(e)[:100]}")

print("\n" + "=" * 70)
print("Setup Status")
print("=" * 70)

print("\n✅ Your Chatbot project is set up correctly!")
print("\n📚 Next steps:")
print("   1. Ingest data:      python ingest_data.py")
print("   2. Run CLI chat:     python main.py")
print("   3. Start API:        uvicorn api:app --reload")
print("   4. Start Frontend:   python ../frontend/app.py")

print("\n" + "=" * 70)
