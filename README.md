# Weather Chat Assistant ☀️

A natural language weather assistant built with Python Flask and deployed on Cloudflare's platform. Ask about the weather in plain English, and get instant results!

## Features

- 🗣️ **Natural Language Processing**: Ask weather questions in plain English
- 🤖 **AI-Powered**: Uses Cloudflare Workers AI to parse queries
- 📜 **Creative Limericks**: AI generates fun weather-themed poems about each city
- 🌍 **Global Coverage**: Get weather for any location worldwide
- 📱 **Beautiful UI**: Modern, responsive web interface
- ⚡ **Fast**: Powered by Cloudflare's global network
- 🔒 **Secure**: API keys stored as environment variables

## Example Queries

- "What's the weather in Riga?"
- "How's the weather in New York tomorrow?"
- "7 day forecast for London in Fahrenheit"
- "What's the temperature in Tokyo today?"

## Technology Stack

- **Backend**: Python Flask
- **AI**: Cloudflare Workers AI (Llama 3)
- **Weather Data**: OpenWeatherMap API
- **Deployment**: Cloudflare Pages/Workers
- **Frontend**: Vanilla JavaScript with modern CSS

## Project Structure

```
weatherapppy/
├── app.py                          # Main Flask application
├── templates/
│   └── chat.html                   # Web interface (HTML/CSS/JS)
├── requirements.txt                # Python dependencies
├── wrangler.toml                   # Cloudflare Workers configuration
├── cloudflare instructions.md      # Detailed deployment guide
└── README.md                       # This file
```

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   # Windows PowerShell
   $env:CF_ACCOUNT_ID="your-cloudflare-account-id"
   $env:CF_API_TOKEN="your-cloudflare-api-token"
   $env:WEATHER_API_KEY="your-openweathermap-api-key"
   
   # Linux/Mac
   export CF_ACCOUNT_ID="your-cloudflare-account-id"
   export CF_API_TOKEN="your-cloudflare-api-token"
   export WEATHER_API_KEY="your-openweathermap-api-key"
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Visit:** http://localhost:8787

### Deployment

See **[cloudflare instructions.md](cloudflare%20instructions.md)** for detailed deployment instructions.

## Environment Variables

You need to set these environment variables:

| Variable | Description | How to Get |
|----------|-------------|------------|
| `CF_ACCOUNT_ID` | Your Cloudflare account ID | Found in Cloudflare Dashboard |
| `CF_API_TOKEN` | Cloudflare API token | Create in Profile → API Tokens |
| `WEATHER_API_KEY` | OpenWeatherMap API key | Sign up at openweathermap.org |

## How It Works

1. **User Input**: User types a natural language weather query
2. **AI Processing**: Cloudflare Workers AI parses the query into structured JSON
3. **JSON Structure**: 
   ```json
   {
     "intent": "get_weather",
     "q": "location",
     "units": "metric|imperial",
     "timeframe": "now|today|tomorrow|7d"
   }
   ```
4. **Weather API**: Fetches weather data from OpenWeatherMap
5. **Limerick Generation**: AI creates a fun poem about the city and weather
6. **Display**: Shows formatted weather information and limerick to the user

## API Response Format

The AI model converts natural language to this JSON structure:

```json
{
  "intent": "get_weather",
  "q": "Paris",
  "units": "metric",
  "timeframe": "now"
}
```

**Defaults:**
- `units`: "metric" (unless Fahrenheit is mentioned)
- `timeframe`: "now" (unless specified otherwise)

## Weather Data Format

Current weather response:
```json
{
  "location": "London, GB",
  "temperature": "15°C",
  "condition": "Partly Cloudy",
  "humidity": 65,
  "wind": "5.2 m/s"
}
```

Forecast response:
```json
{
  "location": "London, GB",
  "forecast": [
    {
      "date": "2026-01-12",
      "condition": "Sunny",
      "high": "18°C",
      "low": "12°C"
    }
  ]
}
```

## Error Handling

The application handles various error cases:

- **Invalid JSON from AI**: Returns "Did not work!"
- **Location not found**: Returns "Location 'X' not found"
- **API errors**: Returns descriptive error messages
- **Missing credentials**: Returns 500 with error message

## Customization

### Customizing the UI

Edit `templates/chat.html` to customize:
- Colors and styling (CSS section)
- Layout and structure (HTML section)
- Behavior and interactions (JavaScript section)

### Using a Different Weather API

To use Weather.com or another provider:

1. Sign up for their API
2. Update the `get_weather()` function in `app.py`
3. Modify the response parsing logic as needed
4. Update the `WEATHER_API_KEY` environment variable

### Using a Different AI Model

Change the model in `call_workers_ai()` in `app.py`:

```python
url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/mistral/mistral-7b-instruct-v0.1"
```

Available models: [Cloudflare AI Models](https://developers.cloudflare.com/workers-ai/models/)

## Contributing

Suggestions and improvements are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is open source and available for personal and commercial use.

## Credits

- Built with [Flask](https://flask.palletsprojects.com/)
- Powered by [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)
- Weather data from [OpenWeatherMap](https://openweathermap.org/)

## Support

For deployment issues, see [cloudflare instructions.md](cloudflare%20instructions.md).

For general questions, check the troubleshooting section in the deployment guide.

---

**Made with ☁️ and ❤️**
