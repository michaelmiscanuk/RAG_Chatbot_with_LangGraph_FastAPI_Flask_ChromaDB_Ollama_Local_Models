"""
Main entry point for the LangGraph Chatbot

This script provides a CLI interface to chat with the bot.
"""

import sys
import uuid
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.graph.workflow import run_workflow


def main():
    print("\n" + "=" * 50)
    print("🤖 LangGraph RAG Chatbot CLI")
    print("=" * 50)
    print("Type 'quit', 'exit', or 'q' to end the session.")
    print("-" * 50)

    thread_id = str(uuid.uuid4())
    print(f"Session ID: {thread_id}\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye! 👋")
                break

            if not user_input:
                continue

            print("Bot: ", end="", flush=True)

            # Run workflow
            try:
                result = run_workflow(input_text=user_input, thread_id=thread_id)

                # Get the last message (AI response)
                messages = result.get("messages", [])
                if messages:
                    last_message = messages[-1]
                    print(last_message.content)
                else:
                    print("No response generated.")

            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

            print("-" * 50)

        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            break


if __name__ == "__main__":
    main()
