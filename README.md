# RAG Chatbot with LangGraph

A full-stack intelligent chatbot application that uses **Retrieval-Augmented Generation (RAG)** to answer questions based on your documents. Built with LangGraph, ChromaDB for vector storage, and Ollama for local LLM inference.

## What Does This App Do?

This chatbot application:
- 📚 **Ingests and stores your documents** in a vector database (ChromaDB)
- 🔍 **Retrieves relevant context** from documents when you ask questions
- 🤖 **Generates intelligent answers** using a local LLM (via Ollama) combined with retrieved information
- 💬 **Maintains conversation history** across multiple interactions
- 🌐 **Provides a web interface** for easy interaction

The RAG approach reduces hallucinations by grounding responses in your actual documents rather than relying solely on the LLM's training data.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Flask Frontend (app.py)                      │ │
│  │  - Web UI (templates/index.html)                         │ │
│  │  - Static assets (CSS/JS)                                │ │
│  │  - API proxy layer                                       │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND API LAYER                        │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              FastAPI Server (api.py)                      │ │
│  │  - /api/chat endpoint                                    │ │
│  │  - CORS middleware                                       │ │
│  │  - Request/Response validation                           │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ invoke
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LANGGRAPH WORKFLOW LAYER                    │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                 LangGraph Workflow                        │ │
│  │                                                           │ │
│  │     START → retrieve → generate → END                    │ │
│  │                                                           │ │
│  │  State: ChatState (messages, context)                    │ │
│  │  Memory: MemorySaver checkpointer                        │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                 │                              │
                 │ retrieval                    │ generation
                 ▼                              ▼
┌──────────────────────────────┐  ┌─────────────────────────────┐
│     DATA LAYER               │  │      LLM LAYER              │
│                              │  │                             │
│  ┌────────────────────────┐  │  │  ┌───────────────────────┐ │
│  │   ChromaDB             │  │  │  │   Ollama LLM          │ │
│  │  - Vector storage      │  │  │  │  - Local inference    │ │
│  │  - Hybrid search       │  │  │  │  - Model presets      │ │
│  │  - Document chunks     │  │  │  │  - Temperature config │ │
│  └────────────────────────┘  │  │  └───────────────────────┘ │
└──────────────────────────────┘  └─────────────────────────────┘
```

## Setup Instructions

### Prerequisites

- **Python 3.11+**
- **Ollama** - For running local LLMs

### Step 1: Install Ollama

1. Visit [https://ollama.ai](https://ollama.ai)
2. Download and install for your OS
3. Start Ollama and pull a model:
   ```bash
   ollama serve
   ollama pull llama3.2
   ```

### Step 2: Set Up the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Set up ChromaDB with your documents:
   ```bash
   python setup_chromadb.py
   ```
   
   This will:
   - Create the ChromaDB vector database
   - Ingest sample documents from `backend/data/`
   - Generate embeddings for semantic search

3. Run the start script (this handles everything else):
   ```bash
   start.bat
   ```
   
   This will:
   - Create a virtual environment
   - Install all required Python packages
   - Start the FastAPI backend server at `http://localhost:8000`

### Step 3: Set Up the Frontend

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Run the start script (this handles everything):
   ```bash
   start.bat
   ```
   
   This will:
   - Create a virtual environment
   - Install all required Python packages
   - Create a `.env` file from the template
   - Start the Flask frontend server at `http://localhost:5000`

### Step 4: Use the Application

1. Open your browser and go to `http://localhost:5000`
2. Type your question in the chat interface
3. The app will:
   - Search your documents for relevant information
   - Generate a context-aware response
   - Display the answer in the chat

## Adding Your Own Documents

1. Place your text files in `backend/data/`
2. Run the setup script again:
   ```bash
   cd backend
   python setup_chromadb.py
   ```
3. Your new documents will be indexed and available for querying

## Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=qwen2.5-coder:0.5b

# LANGSMITH (Optional - for tracing and monitoring)
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT="ips_hackaton_chatbot"

# AZURE (Optional - for Azure OpenAI integration)
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=

# API Configuration
API_BASE_URL=http://localhost:8000
```

### Model Options

You can use different Ollama models by changing the `DEFAULT_MODEL` setting:
- `llama3.2` - Fast, balanced performance
- `llama3.1` - Larger, more capable
- `mistral` - Alternative model option

Install additional models:
```bash
ollama pull mistral
```

## Project Structure

```
├── backend/
│   ├── api.py              # FastAPI server
│   ├── requirements.txt    # Python dependencies
│   ├── setup_chromadb.py   # Database setup script
│   ├── src/
│   │   ├── config/         # Model configuration
│   │   └── graph/          # LangGraph workflow
│   └── data/
│       ├── chroma_db/      # Vector database storage
│       └── sample*.txt     # Sample documents
├── frontend/
│   ├── app.py              # Flask application
│   ├── templates/          # HTML templates
│   └── static/             # CSS and JavaScript
└── README.md               # This file
```

## Technology Stack

- **Backend**: FastAPI, LangGraph, LangChain
- **Frontend**: Flask, Jinja2, JavaScript
- **Vector Database**: ChromaDB
- **LLM**: Ollama (local inference)
- **Workflow Engine**: LangGraph

## Troubleshooting

**Setup fails:**
- Run `start.bat` in both backend and frontend directories
- Make sure Python 3.11+ is installed and in your PATH
- Check your internet connection for downloading packages

**Dependency issues or need to reinstall libraries:**
- Run `backend\reinstall_libraries.bat` to clean and reinstall all backend dependencies
- This will remove the existing virtual environment and reinstall everything fresh

**Backend won't start:**
- Run `python setup_chromadb.py` first in the backend directory
- Then run `start.bat` in the backend directory
- Ensure Ollama is running and has a model installed

**Ollama connection errors:**
- Verify Ollama is running: `ollama serve`
- Check the model is installed: `ollama list`
- Confirm OLLAMA_BASE_URL in your `.env` file

**ChromaDB errors:**
- Delete `backend/data/chroma_db/` and run `python setup_chromadb.py` again
- Check file permissions in the data directory

**Frontend can't connect to backend:**
- Ensure backend is running on port 8000
- Verify API_BASE_URL in frontend configuration
- Check CORS settings in `backend/api.py`

## Features

✅ RAG-based question answering  
✅ Vector similarity search  
✅ Conversational memory  
✅ Local LLM inference (privacy-friendly)  
✅ Web-based user interface  
✅ Easy document ingestion  
✅ Customizable model settings  

## License

MIT License - feel free to use and modify for your needs.
