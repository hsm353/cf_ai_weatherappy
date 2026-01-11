# Quick Start Guide 🚀

Get your Weather Chat Assistant up and running in minutes!

## 🎯 What You'll Build

A natural language weather chatbot that:
- Accepts plain English queries like "What's the weather in Paris?"
- Uses AI to understand the intent
- Fetches real weather data
- Generates creative weather-themed limericks
- Displays results in a beautiful web interface

## ⚡ 5-Minute Local Setup

1. **Get API Keys** (2 minutes)
   - OpenWeatherMap: https://openweathermap.org/api (Free account)
   - Cloudflare Account ID: From your Cloudflare Dashboard
   - Cloudflare API Token: Profile → API Tokens → Create Token

2. **Install Dependencies** (1 minute)
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables** (1 minute)
   
   **Windows (PowerShell):**
   ```powershell
   $env:CF_ACCOUNT_ID="your-account-id"
   $env:CF_API_TOKEN="your-api-token"
   $env:WEATHER_API_KEY="your-weather-key"
   ```
   
   **Linux/Mac:**
   ```bash
   export CF_ACCOUNT_ID="your-account-id"
   export CF_API_TOKEN="your-api-token"
   export WEATHER_API_KEY="your-weather-key"
   ```

4. **Run** (30 seconds)
   ```bash
   python app.py
   ```
   
   Or use the helper scripts:
   - Windows: Double-click `start.bat`
   - Linux/Mac: `chmod +x start.sh && ./start.sh`

5. **Visit** http://localhost:8787 and try it! 🎉

## 🧪 Test Your Setup

Before running the app:
```bash
python test_local.py
```

This verifies all environment variables are set correctly.

## 🌍 Deploy to Cloudflare (10 minutes)

### Quick Deploy

1. **Install Wrangler:**
   ```bash
   npm install -g wrangler
   ```

2. **Login:**
   ```bash
   wrangler login
   ```

3. **Deploy:**
   ```bash
   # For Pages
   wrangler pages project create weather-chat-app
   wrangler pages deploy . --project-name=weather-chat-app
   
   # Or connect via Git (recommended)
   # See cloudflare instructions.md for Git-based deployment
   ```

4. **Set Environment Variables:**
   - Go to Cloudflare Dashboard
   - Workers & Pages → Your Project → Settings
   - Add: `CF_ACCOUNT_ID`, `CF_API_TOKEN`, `WEATHER_API_KEY`

5. **Done!** Your app is live at `https://weather-chat-app.pages.dev`

## 📚 Documentation

- **[cloudflare instructions.md](cloudflare%20instructions.md)** - Complete deployment guide
- **[README.md](README.md)** - Project overview and features
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step checklist

## 🧪 Example Queries to Try

Once your app is running, try these:

1. **Current Weather:**
   - "What's the weather in London?"
   - "How's the weather in Tokyo?"

2. **Specific Timeframes:**
   - "Weather in Paris tomorrow"
   - "7 day forecast for Berlin"

3. **Different Units:**
   - "Weather in New York in Fahrenheit"
   - "Temperature in Los Angeles in imperial units"

4. **Combined:**
   - "What's the 7-day forecast for Sydney in Fahrenheit?"

## ❓ Common Issues

### "Did not work!" error
- Check if all environment variables are set
- Verify API tokens are valid
- Test with a simple city name like "London"

### Location not found
- Use common city names
- Try "City, Country" format: "Paris, France"

### API errors
- Check if you've exceeded free tier limits
- Verify your API keys are active

## 🎨 Customization

- **Change UI/Styling:** Edit `templates/chat.html` (HTML, CSS, JavaScript all in one file)
- **Change AI Model:** Edit `call_workers_ai()` in `app.py`
- **Different Weather API:** Modify `get_weather()` function in `app.py`

## 📞 Need Help?

1. Check the [Troubleshooting section](cloudflare%20instructions.md#troubleshooting) in cloudflare instructions.md
2. Review [Cloudflare's documentation](https://developers.cloudflare.com/)
3. Visit [Cloudflare Community](https://community.cloudflare.com/)

## 🎉 You're All Set!

Your Weather Chat Assistant is ready to go. Enjoy building!

---

**Next Steps:**
- ⭐ Add custom domain
- 📊 Enable analytics
- 🔒 Implement rate limiting
- 💾 Add caching for better performance
