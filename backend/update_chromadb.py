"""
Update ChromaDB Script

This script helps you update the ChromaDB when you add new data to sample0.csv.

Usage:
    python update_chromadb.py
"""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "data"))

from chromadb_manager import upsert_documents_to_chromadb


async def main():
    """Update ChromaDB with new data."""
    print("=" * 70)
    print("ChromaDB Update Script")
    print("=" * 70)
    print()
    print("⚠️  WARNING: This will DELETE the existing ChromaDB collection")
    print("   and recreate it with fresh data from sample0.csv")
    print()

    response = input("Continue? (yes/no): ").strip().lower()

    if response not in ["yes", "y"]:
        print("Update cancelled.")
        return

    print()
    print("Updating ChromaDB...")
    print()

    try:
        # Collection name is auto-generated based on embedding model
        from chromadb_manager import get_chromadb_dir, get_collection_name

        print(
            f"Using embedding model: {os.getenv('EMBEDDING_PROVIDER', 'ollama')} - {os.getenv('EMBEDDING_MODEL', 'nomic-embed-text') if os.getenv('EMBEDDING_PROVIDER', 'ollama') == 'ollama' else os.getenv('AZURE_EMBEDDING_DEPLOYMENT', 'text-embedding-3-small_mimi')}"
        )
        print(f"ChromaDB path: {get_chromadb_dir()}")
        print(f"Collection name: {get_collection_name()}")
        print()

        collection = await upsert_documents_to_chromadb()

        print()
        print("=" * 70)
        print("✅ ChromaDB Updated Successfully!")
        print("=" * 70)
        print()
        print("Your application will now use the updated data.")
        print()

    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ Update Failed: {e}")
        print("=" * 70)
        print()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
