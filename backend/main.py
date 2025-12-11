"""
Main entry point for the LangGraph Text Analysis Workflow

This script demonstrates how to use the workflow with various
input texts and configuration options.
"""

import sys
from pathlib import Path
import textwrap

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.graph.workflow import run_workflow, stream_workflow
from src.utils.helpers import (
    validate_input,
    print_result,
    format_result,
)


def load_sample_inputs():
    """Load sample inputs from txt files in data folder"""
    data_dir = Path(__file__).parent / "data"
    samples = []
    for i in range(5):
        file_path = data_dir / f"sample{i}.txt"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                samples.append(f.read().strip())
        else:
            samples.append("")
    return samples


if __name__ == "__main__":
    # Config for file name
    config_file_name = "sample2.txt"
    
    data_dir = Path(__file__).parent / "data"
    file_path = data_dir / config_file_name
    
    if not file_path.exists():
        print(f"\n❌ Error: Config file {config_file_name} not found in data folder\n")
        sys.exit(1)
    
    with open(file_path, "r", encoding="utf-8") as f:
        input_text = f.read().strip()
    
    # Validate input
    is_valid, error = validate_input(input_text)
    if not is_valid:
        print(f"\n❌ Error: {error}\n")
        sys.exit(1)
    
    # Run workflow
    try:
        print(f"\n🚀 Running workflow with model: qwen2.5-coder:0.5b\n")
        result = run_workflow(
            input_text=input_text, model_name="qwen2.5-coder:0.5b", thread_id="demo"
        )
        
        # Display results
        print_result(result)
        
        # Append to results.txt at the top
        results_file = Path(__file__).parent / "results.txt"
        new_entry = (
            "######################\n"
            "[Our Input]\n"
            f"{textwrap.fill(input_text, width=80)}\n"
            "--------\n"
            "[OUTPUT]\n"
            f"{format_result(result)}\n\n"
        )
        
        # Read existing content
        existing_content = ""
        if results_file.exists():
            with open(results_file, "r", encoding="utf-8") as f:
                existing_content = f.read()
        
        # Write new entry + existing content
        with open(results_file, "w", encoding="utf-8") as f:
            f.write(new_entry + existing_content)
        
        print("\n✅ Workflow completed successfully!\n")
        
    except (ValueError, TypeError, RuntimeError, ConnectionError) as e:
        print(f"\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
