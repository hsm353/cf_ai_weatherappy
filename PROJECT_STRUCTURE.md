# Project Structure 📁

This document explains the organization of the Weather Chat Assistant project.

## File Tree

```
weatherapppy/
│
├── app.py                          # Flask backend application
│   ├── API routes (/chat GET/POST, /)
│   ├── Cloudflare Workers AI integration
│   ├── Weather API integration
│   └── Business logic
│
├── templates/                      # Flask templates folder
│   └── chat.html                   # Frontend web interface
│       ├── HTML structure
│       ├── CSS styling
│       └── JavaScript functionality
│
├── requirements.txt                # Python dependencies
├── wrangler.toml                   # Cloudflare Workers/Pages config
│
├── Documentation/
│   ├── README.md                   # Project overview
│   ├── QUICKSTART.md               # 5-minute setup guide
│   ├── cloudflare instructions.md  # Detailed deployment guide
│   ├── DEPLOYMENT_CHECKLIST.md     # Step-by-step checklist
│   └── PROJECT_STRUCTURE.md        # This file
│
├── Helper Scripts/
│   ├── start.bat                   # Windows startup script
│   ├── start.sh                    # Linux/Mac startup script
│   └── test_local.py               # Environment variable checker
│
└── .gitignore                      # Git ignore rules
```

## Core Files Explained

### `app.py` - Backend Application

The main Flask application that handles:

**Routes:**
- `GET /` - Redirects to /chat
- `GET /chat` - Serves the HTML interface
- `POST /chat` - Processes weather queries

**Functions:**
- `call_workers_ai()` - Calls Cloudflare Workers AI to parse natural language
- `get_weather()` - Fetches weather data from OpenWeatherMap API
- `chat()` - Main route handler

**Key Features:**
- Environment variable handling
- JSON validation
- Error handling
- API integration

### `templates/chat.html` - Frontend Interface

A single-file web interface containing:

**HTML:**
- Input form for user queries
- Result display area
- Example queries section

**CSS:**
- Modern gradient design
- Responsive layout
- Smooth animations
- Mobile-friendly

**JavaScript:**
- Form submission handling
- AJAX requests to backend
- Dynamic result rendering
- Example query population

### `requirements.txt` - Dependencies

Python packages needed:
```
Flask==3.0.0          # Web framework
requests==2.31.0      # HTTP client
gunicorn==21.2.0      # Production server
```

### `wrangler.toml` - Cloudflare Configuration

Cloudflare Workers/Pages deployment settings:
- Project name
- Compatibility date
- Environment configuration

## File Relationships

```
User Browser
     ↓
templates/chat.html (Frontend)
     ↓ (POST /chat)
app.py (Backend)
     ↓
┌────┴────┐
│         │
↓         ↓
Cloudflare    OpenWeatherMap
Workers AI    API
```

## Development Workflow

1. **Local Development:**
   ```bash
   # Edit files
   app.py              # Backend logic
   templates/chat.html # Frontend UI
   
   # Test locally
   python app.py
   # Visit http://localhost:8787
   ```

2. **Deployment:**
   ```bash
   # Ensure all files are committed
   git add .
   git commit -m "Update"
   git push
   
   # Cloudflare Pages auto-deploys from Git
   ```

## Customization Guide

### Change the UI Look & Feel
**Edit:** `templates/chat.html`
- Modify CSS section for colors/fonts
- Update HTML for layout changes
- Adjust JavaScript for behavior

### Change Backend Logic
**Edit:** `app.py`
- Modify `call_workers_ai()` for different AI models
- Update `get_weather()` for different weather APIs
- Adjust route handlers for new features

### Add New Dependencies
**Edit:** `requirements.txt`
```
# Add new line
package-name==version
```

### Change Cloudflare Settings
**Edit:** `wrangler.toml`
- Update project name
- Modify environment settings

## Deployment Files

When deploying to Cloudflare, ensure these files are included:

**Required:**
- ✅ `app.py`
- ✅ `templates/chat.html`
- ✅ `requirements.txt`

**Optional but Recommended:**
- ✅ `wrangler.toml`
- ✅ `.gitignore`
- ✅ Documentation files

**Not Needed:**
- ❌ `test_local.py` (local testing only)
- ❌ `start.bat` / `start.sh` (local development only)
- ❌ `__pycache__/` (auto-generated)

## Environment Variables

Set these in Cloudflare Dashboard (not in files):

```
CF_ACCOUNT_ID      # Your Cloudflare account ID
CF_API_TOKEN       # Cloudflare API token
WEATHER_API_KEY    # OpenWeatherMap API key
```

**Never commit these to Git!**

## Key Design Decisions

### Why Separate HTML File?

**Benefits:**
- ✅ Easier to edit and maintain
- ✅ Better separation of concerns
- ✅ Syntax highlighting in editors
- ✅ Can be edited by frontend developers independently
- ✅ Cleaner Python code

### Why Single HTML File (not split CSS/JS)?

**Benefits:**
- ✅ Simple deployment (one template file)
- ✅ No build process needed
- ✅ All frontend code in one place
- ✅ Faster page loads (no extra requests)

**If you want to split:**
```
templates/
├── chat.html
static/
├── css/
│   └── style.css
└── js/
    └── app.js
```

Then update `chat.html` to link to static files.

## Common Tasks

### Add a New Route
1. Edit `app.py`
2. Add new `@app.route()` decorator
3. Create corresponding template in `templates/`

### Change AI Model
1. Edit `app.py`
2. Find `call_workers_ai()` function
3. Update the model URL

### Customize Colors
1. Edit `templates/chat.html`
2. Find the `<style>` section
3. Modify CSS variables/colors

### Add New Weather Data
1. Edit `app.py` → `get_weather()` function
2. Edit `templates/chat.html` → `formatWeatherResponse()` function

## Troubleshooting

### "Template not found" error
- Ensure `templates/` folder exists
- Ensure `chat.html` is inside `templates/`
- Check file name spelling

### Changes not showing
- Clear browser cache (Ctrl+F5)
- Restart Flask server
- Check if editing correct file

### Deployment issues
- Verify all required files are committed
- Check `templates/` folder is in Git
- Review Cloudflare build logs

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for setup
- Read [cloudflare instructions.md](cloudflare%20instructions.md) for deployment
- Check [README.md](README.md) for features

---

**Questions?** Check the other documentation files or Cloudflare's official docs.
