# Deployment Checklist ✅

Use this checklist to ensure you have everything ready before deploying to Cloudflare.

## Pre-Deployment

- [ ] **Verify Project Structure**
  - Ensure `app.py` exists
  - Ensure `templates/chat.html` exists
  - Ensure `requirements.txt` exists

- [ ] **Get OpenWeatherMap API Key**
  - Sign up at https://openweathermap.org/api
  - Copy your API key
  - Verify it works by testing the API endpoint

- [ ] **Get Cloudflare Account ID**
  - Log in to Cloudflare Dashboard
  - Navigate to Workers & Pages
  - Copy Account ID from the sidebar

- [ ] **Create Cloudflare API Token**
  - Go to Profile → API Tokens
  - Click "Create Token"
  - Use "Edit Cloudflare Workers" template
  - Add permission: Account → Workers AI → Read
  - Copy the token immediately

- [ ] **Test Locally**
  - Run `python test_local.py` to verify environment variables
  - Run `python app.py` (or `start.bat` / `start.sh`)
  - Visit http://localhost:8787
  - Test with a sample query: "What's the weather in London?"

## Deployment Options

### Option 1: Cloudflare Pages (Recommended)

- [ ] **Initialize Git Repository**
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  ```

- [ ] **Push to GitHub/GitLab**
  ```bash
  git remote add origin <your-repo-url>
  git push -u origin main
  ```

- [ ] **Connect to Cloudflare Pages**
  - Go to Cloudflare Dashboard
  - Workers & Pages → Create application → Pages
  - Connect to Git
  - Select your repository
  - Configure build:
    - Build command: `pip install -r requirements.txt`
    - Build output directory: `/`

- [ ] **Set Environment Variables**
  - Go to Settings → Environment variables
  - Add for Production:
    - `CF_ACCOUNT_ID`
    - `CF_API_TOKEN`
    - `WEATHER_API_KEY`

- [ ] **Deploy**
  - Save settings
  - Wait for deployment to complete
  - Test your live URL

### Option 2: Cloudflare Workers

- [ ] **Install Wrangler**
  ```bash
  npm install -g wrangler
  ```

- [ ] **Login to Cloudflare**
  ```bash
  wrangler login
  ```

- [ ] **Set Secrets**
  ```bash
  wrangler secret put CF_ACCOUNT_ID
  wrangler secret put CF_API_TOKEN
  wrangler secret put WEATHER_API_KEY
  ```

- [ ] **Deploy**
  ```bash
  wrangler deploy
  ```

## Post-Deployment

- [ ] **Test Live Application**
  - Visit your deployed URL
  - Try multiple queries:
    - Current weather: "What's the weather in Paris?"
    - Tomorrow: "Weather in Tokyo tomorrow"
    - Forecast: "7 day forecast for Berlin"
    - Imperial units: "Weather in New York in Fahrenheit"

- [ ] **Check Logs**
  - Monitor for errors
  - Verify API calls are working
  - Check response times

- [ ] **Monitor Usage**
  - Check Workers AI usage in Cloudflare dashboard
  - Monitor OpenWeatherMap API calls
  - Verify you're within free tier limits

- [ ] **Set Up Monitoring (Optional)**
  - Enable Cloudflare Web Analytics
  - Set up alerts for errors
  - Monitor performance metrics

## Troubleshooting

If something doesn't work:

1. **Check environment variables** - Most common issue
2. **Review logs** - Use `wrangler pages deployment tail`
3. **Verify API credentials** - Test each API independently
4. **Check Cloudflare status** - Visit cloudflarestatus.com
5. **Read error messages** - They usually point to the issue

## Maintenance

- [ ] **Regular Updates**
  - Update Python dependencies monthly
  - Check for Cloudflare Workers AI model updates
  - Monitor API rate limits

- [ ] **Security**
  - Rotate API tokens every 90 days
  - Review access logs periodically
  - Keep dependencies updated

- [ ] **Optimization**
  - Implement caching for repeated queries
  - Add rate limiting for production
  - Monitor and optimize AI model prompts

## Support Resources

- 📚 [Cloudflare Instructions](cloudflare%20instructions.md) - Detailed guide
- 📖 [README](README.md) - Project overview
- 🌐 [Cloudflare Docs](https://developers.cloudflare.com/)
- 💬 [Cloudflare Community](https://community.cloudflare.com/)

---

**Last Updated:** January 2026

**Need Help?** Check the [cloudflare instructions.md](cloudflare%20instructions.md) for detailed troubleshooting steps.
