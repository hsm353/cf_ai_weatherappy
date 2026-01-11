# Cloudflare Deployment Instructions for Weather Chat App

This guide will walk you through deploying your Python Flask weather chat application to Cloudflare's platform.

## Project Structure

Your application consists of:
- `app.py` - Main Flask backend with API routes and AI integration
- `templates/chat.html` - Frontend interface (HTML/CSS/JavaScript)
- `requirements.txt` - Python dependencies
- `wrangler.toml` - Cloudflare configuration

## Key Features

- Natural language weather queries
- AI-powered query parsing
- Real-time weather data
- **Creative AI-generated limericks** about each city and its weather
- Beautiful responsive UI

## Prerequisites

1. A Cloudflare account (free tier works fine)
2. Node.js and npm installed (for Wrangler CLI)
3. A WeatherAPI.com API key (free tier available)

---

## Step 1: Get Your API Keys

### 1.1 WeatherAPI.com API Key

1. Go to [WeatherAPI.com](https://www.weatherapi.com/signup.aspx)
2. Sign up for a free account
3. After signup, you'll be taken to your dashboard
4. Copy your API key from the dashboard (you'll need this as `WEATHER_API_KEY`)
5. Free tier includes: 1 million calls/month

### 1.2 Cloudflare Account ID and API Token

1. Log in to your [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. **Get your Account ID:**
   - Click on any zone (or go to Workers & Pages)
   - Look for "Account ID" on the right sidebar
   - Copy this ID (you'll need this as `CF_ACCOUNT_ID`)

3. **Create an API Token:**
   - Go to: https://dash.cloudflare.com/profile/api-tokens
   - Click "Create Token"
   - Use the "Edit Cloudflare Workers" template
   - Or create a custom token with these permissions:
     - `Account` → `Workers AI` → `Read`
   - Click "Continue to summary"
   - Click "Create Token"
   - **IMPORTANT:** Copy this token immediately (you'll need this as `CF_API_TOKEN`)

---

## Step 2: Choose Your Deployment Method

Cloudflare offers two main ways to deploy Python applications:

### Option A: Cloudflare Pages (Recommended for Flask apps)
### Option B: Cloudflare Workers with Python

We'll focus on **Option A** as it's more straightforward for Flask applications.

---

## Step 3: Prepare Your Project

1. **Clone or navigate to your project directory:**
   ```bash
   cd weatherapppy
   ```

2. **Note:** This is a Cloudflare Workers Python application. It runs directly on Cloudflare's edge network and doesn't require local Python testing with Flask. You can deploy directly to Cloudflare Workers.

---

## Step 4: Deploy to Cloudflare Pages

### 4.1 Install Wrangler CLI

```bash
npm install -g wrangler
```

### 4.2 Login to Cloudflare

```bash
wrangler login
```

This will open your browser to authenticate with Cloudflare.

### 4.3 Create a Pages Project

Since Cloudflare Pages traditionally uses Git-based deployments, we have two approaches:

#### Approach 1: Using Git (Recommended)

1. **Initialize a Git repository (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub/GitLab:**
   ```bash
   # Create a repo on GitHub, then:
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

3. **Connect to Cloudflare Pages:**
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com/)
   - Click "Workers & Pages"
   - Click "Create application" → "Pages" → "Connect to Git"
   - Select your repository
   - Configure build settings:
     - **Framework preset:** None
     - **Build command:** `pip install -r requirements.txt`
     - **Build output directory:** `/`
   - Click "Save and Deploy"
   
   **Important:** Make sure your deployment includes:
   - `app.py` (main application)
   - `templates/` folder with `chat.html`
   - `requirements.txt`

4. **Set Environment Variables:**
   - After deployment, go to your Pages project
   - Click "Settings" → "Environment variables"
   - Add these variables:
     - `CF_ACCOUNT_ID` = your Cloudflare account ID
     - `CF_API_TOKEN` = your Cloudflare API token
     - `WEATHER_API_KEY` = your OpenWeatherMap API key
   - Click "Save"
   - Redeploy your application

#### Approach 2: Using Wrangler Direct Upload

For direct uploads without Git:

```bash
# Deploy using Wrangler
wrangler pages project create weather-chat-app

# Deploy your files
wrangler pages deploy . --project-name=weather-chat-app
```

---

## Step 5: Verify Deployment

After deployment, test your worker:

1. Visit your worker URL (provided after deployment)
2. Try these queries:
   - "What's the weather in London?"
   - "Weather in Tokyo tomorrow"
   - "7 day forecast for Paris"

3. Check the logs:
   ```bash
   wrangler tail
   ```

---

## Step 6: Update Environment Variables

If you need to update your secrets later:

```bash
# Update any secret
wrangler secret put WEATHER_API_KEY

# List all secrets (won't show values)
wrangler secret list

# Delete a secret
wrangler secret delete SECRET_NAME
```

---

## Step 7: Advanced Configuration

### Custom Domain

Add a custom domain to your worker:

1. Go to your Cloudflare Dashboard
2. Navigate to "Workers & Pages"
3. Select your worker
4. Go to "Triggers" → "Custom Domains"
5. Click "Add Custom Domain"
6. Enter your domain and follow the instructions

### Routes

You can also add routes to serve the worker on your existing domain:

```bash
wrangler route add "example.com/weather/*" --name weather-chat-app
```

---

## Troubleshooting

### Issue: "Did not work!" error

**Possible causes:**
1. **Invalid API credentials:** Double-check your environment variables
2. **Workers AI model not accessible:** Ensure your API token has the correct permissions
3. **Invalid location:** Try a well-known city name

**Debug steps:**
1. Check the browser console (F12) for error messages
2. View Cloudflare logs:
   ```bash
   wrangler pages deployment tail
   ```
3. Verify environment variables are set correctly

### Issue: Worker/Page not found

- Make sure you've deployed the application
- Check if the URL is correct
- Verify the deployment status in your Cloudflare Dashboard

### Issue: Weather API errors

- Verify your WeatherAPI.com API key is valid
- Check if you've exceeded the free tier limits (1M calls/month)
- Ensure the API key is set as a secret via `wrangler secret put`
- Check the API status at weatherapi.com/api-status.aspx

### Issue: Python not supported

If you encounter Python compatibility issues:
1. Use Cloudflare Pages with a Python runtime
2. Consider using a Python WSGI adapter
3. Alternatively, port the application to JavaScript/TypeScript (Workers native language)

---

## Important Notes

### 1. Cloudflare Python Support

As of 2026, Cloudflare has been expanding Python support. Check the latest documentation:
- [Cloudflare Workers Python](https://developers.cloudflare.com/workers/languages/python/)
- [Cloudflare Pages Functions](https://developers.cloudflare.com/pages/functions/)

### 2. Workers AI Models

The application uses the `@cf/meta/llama-3-8b-instruct` model. Other available models:
- `@cf/meta/llama-2-7b-chat-int8`
- `@cf/mistral/mistral-7b-instruct-v0.1`

Check [Cloudflare AI documentation](https://developers.cloudflare.com/workers-ai/models/) for the latest models.

### 3. Cost Considerations

- **Workers AI:** Free tier includes 10,000 neurons per day
- **WeatherAPI.com:** Free tier includes 1,000,000 calls/month
- **Cloudflare Workers:** Free tier includes 100,000 requests/day

### 4. Alternative Weather APIs

If you prefer to use a different provider:
1. Sign up for their API (e.g., OpenWeatherMap, Tomorrow.io)
2. Update the `get_weather()` function in `app.py` with their API endpoints
3. Modify the response parsing logic as needed
4. Update the `WEATHER_API_KEY` secret via `wrangler secret put`

**Why WeatherAPI.com?**
- Simple, clean API design
- Generous free tier (1M calls/month)
- Fast response times
- Reliable uptime

---

## Next Steps

1. **Custom Domain:** Add a custom domain in Cloudflare Pages settings
2. **SSL/TLS:** Cloudflare provides free SSL certificates
3. **Analytics:** Enable Cloudflare Web Analytics in your dashboard
4. **Rate Limiting:** Consider implementing rate limiting for production use
5. **Caching:** Add caching for weather responses to reduce API calls

---

## Additional Resources

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Workers AI Documentation](https://developers.cloudflare.com/workers-ai/)
- [Wrangler CLI Documentation](https://developers.cloudflare.com/workers/wrangler/)

---

## Support

If you encounter issues:
1. Check [Cloudflare Community](https://community.cloudflare.com/)
2. Review [Cloudflare Status](https://www.cloudflarestatus.com/)
3. Contact Cloudflare Support through your dashboard

---

**Happy Deploying! ☁️🌤️**
