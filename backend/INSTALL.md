# Installation Guide

## Prerequisites

1. **UV package manager**
   ```bash
   # Install UV (fast Python package manager)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Verify installation
   uv --version
   ```

2. **Python 3.11 or higher** (UV will handle this automatically)

3. **Ollama installed and running**
   - Download from: https://ollama.ai
   - Or install via package manager:
     - Windows: `winget install Ollama.Ollama`
     - macOS: `brew install ollama`
     - Linux: `curl -fsSL https://ollama.com/install.sh | sh`

## Installation Steps

### Quick Install (Recommended)
```bash
cd backend

# Run the automated installer (includes all steps below)
reinstall_libraries.bat  # Windows
# or
./reinstall_libraries.sh  # Linux/Mac (if available)
```

### Manual Installation

#### 1. Navigate to Backend Directory
```bash
cd backend
```

#### 2. Create Virtual Environment with UV
```bash
# UV creates and activates the virtual environment automatically
uv venv
```

#### 3. Install Dependencies
```bash
# Install the project and all dependencies
uv pip install -e .
```

This will install:
- `langgraph>=0.2.62` - The LangGraph framework
- `langchain>=0.3.18` - LangChain core
- `langchain-ollama>=0.2.0` - Ollama integration
- `langchain-core>=0.3.29` - Core components
- `typing-extensions>=4.12.0` - Type hints support

#### 4. Start Ollama
```bash
ollama serve
```

#### 5. Pull a Model
```bash
ollama pull llama3.2
```

Available models:
- `llama3.2` - Recommended, good balance
- `llama3.2:1b` - Smaller, faster
- `mistral` - Alternative option
- `codellama` - For code-related tasks

#### 6. Verify Installation
```bash
python test_setup.py
```

You should see all tests passing ✅

#### 7. Run the Demo
```bash
python main.py
```

## Troubleshooting

### Issue: UV not installed
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on Windows with winget
winget install astral-sh.uv

# Verify
uv --version
```

### Issue: Python version too old
```bash
# UV will automatically download the correct Python version
# Check what UV is using
uv python list
```

### Issue: Ollama connection refused
```bash
# Make sure Ollama is running
ollama serve

# Check if running
curl http://localhost:11434/api/version
```

### Issue: Model not found
```bash
# List installed models
ollama list

# Pull the model
ollama pull llama3.2
```

### Issue: Import errors after installation
```bash
# Ensure virtual environment is activated
# UV automatically activates when you run commands

# Reinstall
uv pip install -e . --force-reinstall
```

## Optional: Development Tools

For development, install additional tools:

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Or manually
uv pip install black isort flake8 mypy pytest pytest-asyncio pytest-cov
```

## Platform-Specific Notes

### Windows
- Use `reinstall_libraries.bat` for automated setup
- UV works seamlessly with Windows
- May need to run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### macOS
- Use Homebrew for Ollama: `brew install ollama`
- UV works great on macOS

### Linux
- May need to install Python dev headers if building packages
- UV handles most dependencies automatically

## Verification Checklist

Before using the project, verify:

- [ ] UV installed (`uv --version`)
- [ ] Virtual environment created (`.venv` folder exists)
- [ ] Dependencies installed (`uv pip list` shows langgraph, langchain, etc.)
- [ ] Ollama running (`curl http://localhost:11434`)
- [ ] Model downloaded (`ollama list` shows llama3.2)
- [ ] Test script passes (`python test_setup.py`)
- [ ] Demo runs (`python main.py`)

## What's Next?

After installation:
1. Read `GETTING_STARTED.md` for usage guide
2. Run examples: `cd examples && python examples.py`
3. Explore the code in `src/` folder
4. Check `ARCHITECTURE.md` for technical details

## Getting Help

If you're stuck:
1. Run `python test_setup.py` to diagnose
2. Check error messages carefully
3. Verify Ollama is running: `ollama serve`
4. Try the quickstart: `python quickstart.py`

## Uninstallation

To remove the project:

```bash
# Remove virtual environment
rm -rf .venv  # Linux/Mac
rmdir /s .venv  # Windows

# Remove __pycache__ directories
find . -type d -name __pycache__ -exec rm -rf {} +  # Linux/Mac
```

Ollama can be uninstalled separately using your system's package manager.
