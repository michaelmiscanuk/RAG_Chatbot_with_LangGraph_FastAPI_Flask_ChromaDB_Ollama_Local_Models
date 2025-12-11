# 🎯 Text Analysis Application - Full Stack

A modern, full-stack AI-powered text analysis application with beautiful UI and intelligent backend. Analyze any text to get instant summaries and sentiment analysis using LangGraph workflows and LLM models.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey.svg)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange.svg)

## ✨ Features

### Frontend
- 🎨 **Beautiful Modern UI** - Gradient backgrounds, smooth animations, responsive design
- ⚡ **Fast & Intuitive** - Real-time character counter, instant feedback
- 📱 **Mobile Friendly** - Works perfectly on all devices
- 🎯 **User-Focused** - Sample texts, helpful error messages, loading states
- 🌙 **Dark Theme** - Easy on the eyes

### Backend
- 🤖 **LangGraph Workflows** - Multi-node processing pipeline
- 🧠 **Multiple AI Models** - Choose from various Ollama models
- 📊 **Comprehensive Analysis** - Word count, summary, sentiment
- 🔌 **REST API** - Clean, documented FastAPI endpoints
- 🔒 **Secure** - CORS enabled, input validation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      USER BROWSER                        │
│                  (Beautiful Modern UI)                   │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ HTTP/JSON
                        │
┌───────────────────────▼─────────────────────────────────┐
│                  FRONTEND (Vercel)                       │
│                                                          │
│  • Flask Web Server                                     │
│  • Modern CSS3 + Vanilla JS                            │
│  • API Proxy to Backend                                │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ REST API
                        │
┌───────────────────────▼─────────────────────────────────┐
│                 BACKEND (Render.com)                     │
│                                                          │
│  • FastAPI REST API                                     │
│  • LangGraph Workflow:                                  │
│    ├─ Node 1: Input Processing                         │
│    └─ Node 2: LLM Analysis                             │
│  • Ollama Integration                                   │
└─────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
langgraph_test1/
├── backend/                    # FastAPI Backend
│   ├── api.py                 # FastAPI app with endpoints
│   ├── main.py                # Original CLI app
│   ├── requirements.txt       # Backend dependencies
│   ├── render.yaml           # Render deployment config
│   ├── DEPLOYMENT.md         # Backend deployment guide
│   └── src/
│       ├── config/           # Model configuration
│       ├── graph/            # LangGraph workflow
│       │   ├── nodes.py     # Processing nodes
│       │   ├── state.py     # State management
│       │   └── workflow.py  # Workflow definition
│       └── utils/           # Helper functions
│
└── frontend/                  # Flask Frontend
    ├── app.py                # Flask application
    ├── requirements.txt      # Frontend dependencies
    ├── vercel.json          # Vercel deployment config
    ├── README.md            # Frontend documentation
    ├── static/
    │   ├── css/
    │   │   └── style.css    # Beautiful global styles
    │   └── js/
    │       └── main.js      # Frontend JavaScript
    └── templates/
        ├── index.html       # Main page
        ├── about.html       # About page
        ├── 404.html        # 404 error page
        └── 500.html        # 500 error page
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Ollama installed and running (for local development)
- Git
- Node.js (for Vercel CLI, optional)

### Local Development

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd langgraph_test1
```

#### 2. Start Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start Ollama (separate terminal)
ollama serve

# Pull a model
ollama pull qwen2.5-coder:0.5b

# Start backend
python api.py
```

Backend will run at `http://localhost:8000`

#### 3. Start Frontend

```bash
cd frontend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment
copy .env.example .env
# Edit .env and set API_BASE_URL=http://localhost:8000

# Start frontend
python app.py
```

Frontend will run at `http://localhost:5000`

#### 4. Test the Application

1. Open browser: `http://localhost:5000`
2. Enter some text
3. Click "Analyze Text"
4. View results!

## 🌐 Deployment

### Backend Deployment (Render.com)

1. **Create Render Account**: [render.com](https://render.com)

2. **Deploy Backend**:
   - Create new Web Service
   - Connect GitHub repository
   - Set root directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn api:app --host 0.0.0.0 --port $PORT`

3. **Configure Environment Variables**:
   ```
   PYTHON_VERSION=3.11.0
   OLLAMA_BASE_URL=<your-ollama-server>
   ```

4. **Get Backend URL**: `https://your-app.onrender.com`

📖 **Detailed Guide**: See `backend/DEPLOYMENT.md`

### Frontend Deployment (Vercel)

1. **Install Vercel CLI** (optional):
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

3. **Set Environment Variables** in Vercel Dashboard:
   ```
   API_BASE_URL=https://your-backend.onrender.com
   SECRET_KEY=<random-secure-string>
   FLASK_ENV=production
   ```

4. **Update CORS** in `backend/api.py`:
   ```python
   allow_origins=[
       "https://your-frontend.vercel.app",
   ]
   ```

📖 **Detailed Guide**: See `frontend/README.md`

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Analyze text
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is amazing! I love it.",
    "model_name": "qwen2.5-coder:0.5b"
  }'

# View API docs
# Open: http://localhost:8000/docs
```

### Test Frontend

1. Open `http://localhost:5000`
2. Try sample texts
3. Test with long text (>10,000 characters should show error)
4. Test different models
5. Check responsive design on mobile

## 📊 API Endpoints

### Backend (FastAPI)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/api/analyze` | POST | Analyze text |
| `/api/models` | GET | List available models |
| `/docs` | GET | Swagger UI |

### Frontend (Flask)

| Route | Description |
|-------|-------------|
| `/` | Main analysis page |
| `/about` | About page |
| `/health` | Health check |
| `/api/analyze` | Proxy to backend |
| `/api/models` | Proxy to backend |

## 🔧 Configuration

### Backend Environment Variables

```env
PYTHON_VERSION=3.11.0
OLLAMA_BASE_URL=http://localhost:11434
PORT=8000
```

### Frontend Environment Variables

```env
API_BASE_URL=http://localhost:8000
SECRET_KEY=your-secret-key
FLASK_ENV=development
```

## 🎨 Customization

### Modify Styles

Edit `frontend/static/css/style.css`:

```css
:root {
    --primary-color: #6366f1;  /* Change primary color */
    --secondary-color: #ec4899; /* Change secondary color */
    /* ... more variables ... */
}
```

### Add New Models

Edit `backend/src/config/models.py`:

```python
AVAILABLE_MODELS = {
    "your-model": {
        "name": "your-model",
        "temperature": 0.7,
    }
}
```

### Modify Workflow

Edit `backend/src/graph/nodes.py` and `backend/src/graph/workflow.py` to add new processing nodes or change the workflow logic.

## 📈 Performance

- **Backend**: FastAPI is one of the fastest Python frameworks
- **Frontend**: Lightweight Flask with minimal dependencies
- **UI**: No framework bloat, pure CSS and vanilla JS
- **Cold Start**: ~30-60 seconds on free tier (Render)
- **Response Time**: ~2-5 seconds for analysis (depends on model)

## 🛡️ Security

- ✅ CORS properly configured
- ✅ Input validation on both frontend and backend
- ✅ Environment variables for sensitive data
- ✅ No data persistence (privacy-first)
- ✅ HTTPS on both Vercel and Render
- ✅ Rate limiting (can be added)

## 🐛 Troubleshooting

### "Cannot connect to backend"

1. Check if backend is running
2. Verify `API_BASE_URL` in frontend `.env`
3. Check CORS settings
4. Review backend logs

### "Analysis taking too long"

1. Try smaller text
2. Use faster model (qwen2.5-coder:0.5b)
3. Check Ollama is running
4. Verify server resources

### Deployment Issues

1. Check deployment logs
2. Verify environment variables
3. Ensure Python version compatibility
4. Review requirements.txt

## 📚 Documentation

- [Backend Deployment Guide](backend/DEPLOYMENT.md)
- [Frontend Documentation](frontend/README.md)
- [Backend Architecture](backend/ARCHITECTURE.md)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **LangGraph** - For workflow orchestration
- **FastAPI** - For modern API framework
- **Flask** - For simple frontend framework
- **Ollama** - For local LLM inference
- **Vercel** - For frontend hosting
- **Render** - For backend hosting

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting sections
- Review documentation

---

**Built with ❤️ using Python, FastAPI, Flask, LangGraph, and Modern CSS**

Happy analyzing! 🎉
