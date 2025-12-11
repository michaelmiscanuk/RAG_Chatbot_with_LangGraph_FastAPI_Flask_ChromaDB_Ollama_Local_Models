# Text Analysis Frontend 🎨

Beautiful, modern web interface for the LangGraph Text Analysis application. Built with Flask and deployed on Vercel.

## Features

- 🎨 **Beautiful UI**: Modern design with gradients, animations, and responsive layout
- ⚡ **Fast & Responsive**: Optimized for all devices
- 🔌 **API Integration**: Seamless communication with FastAPI backend
- 📊 **Real-time Stats**: Character count, word count, and instant feedback
- 🎯 **User-Friendly**: Clean interface with sample texts and helpful error messages

## Tech Stack

- **Flask** - Lightweight Python web framework
- **Modern CSS3** - Custom styles with CSS variables, gradients, and animations
- **Vanilla JavaScript** - Clean, dependency-free frontend code
- **Google Fonts** - Inter font family for beautiful typography

## Project Structure

```
frontend/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel deployment config
├── .env.example           # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css      # Global styles
│   └── js/
│       └── main.js        # Frontend JavaScript
└── templates/
    ├── index.html         # Main page
    ├── about.html         # About page
    ├── 404.html          # 404 error page
    └── 500.html          # 500 error page
```

## Local Development

### Prerequisites

- Python 3.11 or higher
- Backend API running (see backend README)

### Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and set:
   ```
   API_BASE_URL=http://localhost:8000
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open in browser**:
   ```
   http://localhost:5000
   ```

## Deployment to Vercel

### Option 1: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd frontend
   vercel
   ```

4. **Set environment variables** in Vercel Dashboard:
   - `API_BASE_URL`: Your backend URL (from Render)
   - `SECRET_KEY`: Generate a secure random string
   - `FLASK_ENV`: production

### Option 2: Deploy via GitHub

1. **Push code to GitHub**:
   ```bash
   git add .
   git commit -m "Add frontend"
   git push origin main
   ```

2. **Import project in Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Add environment variables:
     - `API_BASE_URL`: Your backend URL
     - `SECRET_KEY`: Secure random string
     - `FLASK_ENV`: production
   - Deploy!

3. **Update backend CORS**:
   After deployment, update the CORS settings in `backend/api.py` to include your Vercel URL:
   ```python
   allow_origins=[
       "https://your-app.vercel.app",
       "http://localhost:5000",
   ]
   ```

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `API_BASE_URL` | Backend API URL | `https://your-backend.onrender.com` |
| `SECRET_KEY` | Flask secret key | Random string |
| `FLASK_ENV` | Environment | `development` or `production` |

### Custom Styling

All styles are in `static/css/style.css`. The design uses CSS variables for easy customization:

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #ec4899;
    --accent-color: #14b8a6;
    /* ... more variables ... */
}
```

## API Endpoints

The frontend proxies these endpoints to the backend:

- `POST /api/analyze` - Analyze text
- `GET /api/models` - Get available models
- `GET /health` - Health check

## Testing

### Test Locally

1. Start backend: `cd backend && python api.py`
2. Start frontend: `cd frontend && python app.py`
3. Open `http://localhost:5000`
4. Try analyzing sample texts

### Test Health Endpoint

```bash
curl http://localhost:5000/health
```

## Troubleshooting

### Cannot connect to backend

**Problem**: Frontend shows "Cannot connect to backend API"

**Solutions**:
1. Check if backend is running
2. Verify `API_BASE_URL` in `.env`
3. Check CORS settings in backend
4. Verify network connectivity

### Styles not loading

**Problem**: Page appears unstyled

**Solutions**:
1. Check browser console for errors
2. Verify static files are being served
3. Clear browser cache
4. Check `static/css/style.css` exists

### Deployment fails on Vercel

**Problem**: Build or deployment errors

**Solutions**:
1. Check Python version in `vercel.json`
2. Verify all dependencies in `requirements.txt`
3. Check Vercel logs for specific errors
4. Ensure `app.py` is in the root of deployment directory

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS/Android)

## Performance

- Optimized CSS with minimal dependencies
- Vanilla JavaScript (no framework overhead)
- Efficient API calls with loading states
- Responsive images and assets

## Security

- CORS properly configured
- Environment variables for sensitive data
- Input validation on frontend and backend
- No data persistence (privacy-focused)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions:
- Check the troubleshooting section
- Review backend README
- Open an issue on GitHub

---

Built with ❤️ using Flask, Modern CSS, and Vanilla JavaScript
