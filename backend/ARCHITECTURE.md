# LangGraph Workflow Architecture

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     LangGraph Workflow                          │
│                  Text Analysis Pipeline                         │
└─────────────────────────────────────────────────────────────────┘

                              START
                                │
                                ▼
                    ┌───────────────────────┐
                    │                       │
                    │   INPUT_PROCESSOR     │
                    │                       │
                    │  Reads: input_text    │
                    │  Writes: word_count   │
                    │                       │
                    └───────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │                       │
                    │     SUMMARIZER        │
                    │                       │
                    │  Reads: input_text    │
                    │         word_count    │
                    │  Writes: summary      │
                    │          sentiment    │
                    │                       │
                    └───────────────────────┘
                                │
                                ▼
                              END
```

## State Flow

```
Initial State:
┌─────────────────────────────────┐
│ input_text: "User's text..."   │
│ word_count: -                   │
│ summary: -                      │
│ sentiment: -                    │
└─────────────────────────────────┘

After INPUT_PROCESSOR:
┌─────────────────────────────────┐
│ input_text: "User's text..."   │
│ word_count: 42                  │  ← Updated
│ summary: -                      │
│ sentiment: -                    │
└─────────────────────────────────┘

After SUMMARIZER (Final):
┌─────────────────────────────────┐
│ input_text: "User's text..."   │
│ word_count: 42                  │
│ summary: "Brief summary..."     │  ← Updated
│ sentiment: "positive"           │  ← Updated
└─────────────────────────────────┘
```

## Component Architecture

```
backend/
│
├── src/
│   │
│   ├── config/
│   │   └── models.py
│   │       ├── ModelConfig class
│   │       ├── get_model(model_name) → ChatOllama
│   │       ├── get_model_from_preset(preset) → ChatOllama
│   │       └── MODEL_PRESETS dict
│   │
│   ├── graph/
│   │   ├── state.py
│   │   │   └── TextAnalysisState (TypedDict)
│   │   │       ├── input_text: str
│   │   │       ├── word_count: int
│   │   │       ├── summary: str
│   │   │       └── sentiment: str
│   │   │
│   │   ├── nodes.py
│   │   │   ├── input_processor(state) → dict
│   │   │   ├── summarizer(state, model_name) → dict
│   │   │   └── create_summarizer_node(model_name) → function
│   │   │
│   │   └── workflow.py
│   │       ├── create_workflow(model_name, use_checkpointer) → CompiledGraph
│   │       ├── run_workflow(input_text, model_name, thread_id) → State
│   │       └── stream_workflow(input_text, model_name, thread_id) → Iterator
│   │
│   └── utils/
│       └── helpers.py
│           ├── validate_input(text) → (bool, error)
│           ├── format_result(state, format_type) → str
│           ├── print_result(state, format_type) → None
│           └── create_sample_inputs() → list[str]
│
├── main.py              # CLI entry point
├── test_setup.py        # Setup verification
├── quickstart.py        # Quick start script
└── examples/
    └── examples.py      # Usage examples
```

## Data Flow Details

### Input Processing Node
```python
def input_processor(state: TextAnalysisState) -> dict:
    """
    Input:  state["input_text"] → str
    Logic:  Split text, count words
    Output: {"word_count": int}
    """
```

### Summarizer Node
```python
def summarizer(state: TextAnalysisState, model_name: str) -> dict:
    """
    Input:  state["input_text"] → str
            state["word_count"] → int
    Logic:  
        1. Initialize LLM model
        2. Generate summary using model
        3. Generate sentiment using model
    Output: {
        "summary": str,
        "sentiment": str
    }
    """
```

## LangGraph Features Used

### 1. State Management
- **TypedDict Schema**: `TextAnalysisState`
- **State Updates**: Each node returns dict with updates
- **State Persistence**: All fields accessible across nodes

### 2. Graph Construction
```python
builder = StateGraph(TextAnalysisState)
builder.add_node("input_processor", input_processor)
builder.add_node("summarizer", summarizer_node)
builder.add_edge(START, "input_processor")
builder.add_edge("input_processor", "summarizer")
builder.add_edge("summarizer", END)
```

### 3. Checkpointing & Memory
```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# Persistent conversations with thread_id
result = graph.invoke(
    {"input_text": "..."},
    {"configurable": {"thread_id": "user-123"}}
)
```

### 4. Streaming Support
```python
for update in graph.stream(
    {"input_text": "..."},
    stream_mode="updates"
):
    print(update)  # Real-time updates from each node
```

## Model Configuration

```
ModelConfig
    ↓
┌─────────────────────────┐
│ model_name: "llama3.2" │
│ temperature: 0.7        │
│ base_url: localhost     │
│ num_ctx: 2048           │
│ top_p: 0.9              │
│ top_k: 40               │
└─────────────────────────┘
    ↓
ChatOllama Instance
```

### Preset Configurations
```
creative:      temp=0.9, top_p=0.95  (more random)
balanced:      temp=0.7, top_p=0.9   (default)
precise:       temp=0.3, top_p=0.8   (more focused)
deterministic: temp=0.0, top_p=1.0   (reproducible)
```

## Execution Flow

### Standard Invocation
```
1. User calls: run_workflow("text...")
2. Create workflow with model config
3. Initialize state: {"input_text": "text..."}
4. Execute input_processor node
5. Update state with word_count
6. Execute summarizer node
7. Update state with summary & sentiment
8. Return final state
```

### Streaming Invocation
```
1. User calls: stream_workflow("text...")
2. Create workflow
3. Initialize state
4. Yield update from input_processor
5. Yield update from summarizer
6. Stream completes
```

## Error Handling

```
┌─────────────────────────┐
│  Validation Layer       │
│  (validate_input)       │
└─────────────────────────┘
           ↓
┌─────────────────────────┐
│  Node Execution         │
│  (try-except blocks)    │
└─────────────────────────┘
           ↓
┌─────────────────────────┐
│  Result Formatting      │
│  (error messages)       │
└─────────────────────────┘
```

## Extension Points

### Add New Node
```python
def new_analysis_node(state: TextAnalysisState) -> dict:
    # Your logic here
    return {"new_field": value}

# Add to workflow
builder.add_node("new_analysis", new_analysis_node)
builder.add_edge("summarizer", "new_analysis")
builder.add_edge("new_analysis", END)
```

### Add Conditional Routing
```python
def router(state: TextAnalysisState) -> str:
    if state["word_count"] > 100:
        return "detailed_analysis"
    return "quick_analysis"

builder.add_conditional_edges(
    "input_processor",
    router,
    {
        "detailed_analysis": "detailed_node",
        "quick_analysis": "quick_node"
    }
)
```

### Add Custom Reducers
```python
from typing import Annotated
import operator

class ExtendedState(TypedDict):
    messages: Annotated[list, operator.add]  # Append messages
    count: Annotated[int, operator.add]      # Sum counts
```

## Use Cases

1. **Content Moderation**: Analyze user-generated content
2. **Document Processing**: Summarize and categorize documents
3. **Customer Feedback**: Analyze sentiment in reviews
4. **Email Automation**: Summarize and prioritize emails
5. **Research Assistant**: Process and summarize papers

## Performance Considerations

- **Model Selection**: Choose appropriate model for task
- **Temperature**: Adjust for creativity vs consistency
- **Context Window**: Larger context for longer texts
- **Streaming**: Use for real-time feedback
- **Checkpointing**: Enable for production deployments
