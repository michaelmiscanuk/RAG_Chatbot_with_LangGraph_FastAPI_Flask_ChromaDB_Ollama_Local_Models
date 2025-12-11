# LangGraph Text Analysis Workflow

A comprehensive LangGraph implementation demonstrating a multi-node workflow for text analysis using Ollama models.

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── models.py          # Model configuration
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py            # State definition
│   │   ├── nodes.py            # Node implementations
│   │   └── workflow.py         # Graph definition
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Helper functions
├── main.py                     # Main entry point
├── requirements.txt
└── README.md
```

## Features

- **State Management**: TypedDict-based state with 3 distinct fields
- **Multi-Node Workflow**: 2-node processing pipeline
  - Input Processor: Analyzes text and counts words
  - Summarizer: Generates summary and sentiment analysis
- **Ollama Integration**: Configurable model selection
- **Memory Persistence**: Built-in checkpointing with MemorySaver
- **Comprehensive Logging**: Detailed execution tracking

## Use Case

This workflow implements a text analysis system:
1. User provides input text
2. Node 1 processes the input and calculates metadata (word count)
3. Node 2 reads the text and metadata to generate:
   - A concise summary
   - Sentiment analysis

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running:
```bash
ollama serve
```

3. Pull required models:
```bash
ollama pull llama3.2
```

4. Create `.env` file (optional):
```bash
cp .env.example .env
```

## Usage

Run the workflow:
```bash
python main.py
```

Or import and use programmatically:
```python
from src.graph.workflow import create_workflow

# Create workflow with default model
workflow = create_workflow()

# Or specify a model
workflow = create_workflow(model_name="llama3.2")

# Run the workflow
result = workflow.invoke({
    "input_text": "Your text here..."
})
```

## Configuration

Models are configured in `src/config/models.py`. You can:
- Change the default model
- Add new model configurations
- Adjust model parameters (temperature, etc.)

## Requirements

- Python 3.11+
- Ollama installed and running
- At least one Ollama model pulled
