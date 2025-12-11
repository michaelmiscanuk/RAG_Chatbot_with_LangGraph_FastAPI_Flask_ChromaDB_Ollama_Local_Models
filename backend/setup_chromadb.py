"""
Setup script to initialize ChromaDB with CSV data

This script loads data from sample0.csv and creates a ChromaDB collection
with hybrid search capabilities.

Usage:
    python setup_chromadb.py
"""

import asyncio
import os
import sys
import shutil
from pathlib import Path

# Add data directory to path
sys.path.insert(0, str(Path(__file__).parent / "data"))

from chromadb_manager import upsert_documents_to_chromadb


async def main():
    """Main setup function."""
    print("=" * 70)
    print("ChromaDB Setup Script")
    print("=" * 70)
    print()
    print("This script will:")
    print("  1. Load data from backend/data/sample0.csv")
    print("  2. Create ChromaDB with embeddings")
    print("  3. Test hybrid search capabilities")
    print()
    print("=" * 70)
    print()

    try:
        # Get the dynamic ChromaDB path based on embedding model
        from chromadb_manager import get_chromadb_dir, get_collection_name

        chroma_db_path = get_chromadb_dir()
        collection_name = get_collection_name()

        print(
            f"Using embedding model: {os.getenv('EMBEDDING_PROVIDER', 'ollama')} - {os.getenv('EMBEDDING_MODEL', 'nomic-embed-text') if os.getenv('EMBEDDING_PROVIDER', 'ollama') == 'ollama' else os.getenv('AZURE_EMBEDDING_DEPLOYMENT', 'text-embedding-3-small_mimi')}"
        )
        print(f"ChromaDB path: {chroma_db_path}")
        print(f"Collection name: {collection_name}")
        print()

        # Clean up any corrupted ChromaDB database
        if chroma_db_path.exists():
            print(f"Removing existing ChromaDB at {chroma_db_path}...")
            try:
                shutil.rmtree(chroma_db_path)
                print("✅ Cleaned up existing database")
            except Exception as e:
                print(f"⚠️  Warning: Could not remove existing database: {e}")
            print()

        # Create and populate ChromaDB (collection_name auto-generated)
        collection = await upsert_documents_to_chromadb()

        print()
        print("=" * 70)
        print("✅ ChromaDB Setup Complete!")
        print("=" * 70)
        print()
        print("You can now run your application with:")
        print("  cd backend")
        print("  python -m uvicorn api:app --reload")
        print()
        print("Or use the start script:")
        print("  cd backend")
        print("  ./start.bat  (Windows)")
        print("  ./start.sh   (Linux/Mac)")
        print()

    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ Setup Failed: {e}")
        print("=" * 70)
        print()
        print("Make sure you have:")
        print("  1. Created backend/data/sample0.csv")
        print("  2. Configured Azure OpenAI credentials in .env")
        print()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
