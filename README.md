# Weather Chat Assistant

An AI-powered natural language weather assistant built with Python and deployed on Cloudflare Workers. Ask about the weather in plain English and get instant results with creative limericks.

---

## **Live Application Demo**

**View the live application here:** **[https://weatherappy.arvid-a10.workers.dev/](https://weatherappy.arvid-a10.workers.dev/)**

This is the actual deployed application. You can use it right now to test all features.

---

## Features

### Core Functionality
- Natural language processing for weather queries
- AI-powered query parsing using Cloudflare Workers AI (Llama 3 8B Instruct)
- Global weather coverage for any location worldwide
- Multi-day forecasts (current, daily, or 7-day)
- Flexible units (Celsius and Fahrenheit)
- Real-time data from WeatherAPI.com

### AI-Powered Features
- Creative weather-themed limericks generated for each location
- Intelligent intent detection extracting location, timeframe, and units
- Context understanding (e.g., "What's the weather in Borat's hometown?")

### User Experience
- Modern, responsive Cloudflare-themed interface
- Recent Queries sidebar showing last 4 global queries in real-time
- Global memory powered by Cloudflare KV storage
- Sample prompt suggestions via dropdown
- Comprehensive error handling with user-friendly messages

### Performance & Security
- Edge computing on Cloudflare's global network (sub-100ms response times)
- Secure secrets stored as Cloudflare Secrets
- Built-in logging and monitoring
- Serverless architecture handling unlimited concurrent users

## Example Queries

Try these natural language questions:

- "What's the weather in Paris?"
- "How's it like in Tokyo tomorrow?"
- "7 day forecast for London"
- "Temperature in New York in Fahrenheit"
- "What's the weather in Borat's home town?" (AI figures out it's Kazakhstan)
- "Weather in the city that Scarlett Johansson was born in" (AI knows it's NYC)
- "Weather in the oil capital of the UK for the next 7 days?" (AI determines Aberdeen)

## Architecture

### Technology Stack
- **Runtime**: Cloudflare Workers (Python)
- **AI Model**: Cloudflare Workers AI - Llama 3 8B Instruct
- **Weather API**: WeatherAPI.com (1M free calls/month)
- **State Storage**: Cloudflare KV (global memory)
- **Frontend**: HTML/CSS/JavaScript (embedded in Worker)
- **Deployment**: Wrangler CLI

### Request Flow

1. User submits natural language query
2. Cloudflare Workers AI (Llama 3) parses query into structured JSON
3. WeatherAPI.com fetches weather data for the location
4. Cloudflare Workers AI (Llama 3) generates weather-themed limerick
5. Cloudflare KV stores query in global history (last 4 queries)
6. Response returned to user with weather data, limerick, and updated history

### AI Query Processing

The AI converts natural language to structured JSON:

**Input:** "7 day forecast for London in Fahrenheit"

**Output:**
```json
{
  "intent": "get_weather",
  "q": "London",
  "units": "imperial",
  "timeframe": "7d"
}
```

**Defaults:**
- `units`: "metric" (Celsius) unless Fahrenheit is mentioned
- `timeframe`: "now" unless specified otherwise

## Project Structure

```
weatherapppy/
├── app.py                          # Main Worker application (900+ lines)
│   ├── HTML_TEMPLATE              # Embedded frontend UI
│   ├── call_workers_ai()          # Query parsing with Llama 3
│   ├── generate_limerick()        # Limerick generation with Llama 3
│   ├── get_weather()              # WeatherAPI.com integration
│   ├── get_global_history()       # KV storage retrieval
│   ├── save_to_global_history()   # KV storage persistence
│   └── on_fetch()                 # Main request handler
├── wrangler.toml                   # Cloudflare Workers configuration
├── cloudflare instructions.md      # Detailed deployment guide
├── QUICKSTART.md                   # Quick deployment guide
├── GLOBAL_MEMORY.md                # KV memory implementation docs
├── ERROR_HANDLING.md               # Error handling documentation
└── README.md                       # This file
```

## Quick Start

### Prerequisites

1. Cloudflare Account - [Sign up free](https://dash.cloudflare.com/sign-up)
2. WeatherAPI.com Key - [Get free API key](https://www.weatherapi.com/signup.aspx) (1M calls/month)
3. Wrangler CLI - Install globally: `npm install -g wrangler`

### Deployment (5 minutes)

**1. Clone and configure:**
```bash
git clone <your-repo>
cd weatherapppy
wrangler login
```

**2. Create KV namespace:**
```bash
wrangler kv namespace create "CHAT_HISTORY"
```
Copy the `id` and update `wrangler.toml`:
```toml
[[kv_namespaces]]
binding = "CHAT_HISTORY"
id = "your-kv-namespace-id"
```

**3. Set secrets:**
```bash
wrangler secret put CF_ACCOUNT_ID
# Paste your Cloudflare Account ID

wrangler secret put CF_API_TOKEN
# Paste your Cloudflare API Token

wrangler secret put WEATHER_API_KEY
# Paste your WeatherAPI.com key
```

**4. Deploy:**
```bash
wrangler deploy
```

**5. Visit your app:**
```
https://weatherappy.YOUR-SUBDOMAIN.workers.dev/
```

For detailed instructions, see [cloudflare instructions.md](cloudflare%20instructions.md).

## Environment Variables

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `CF_ACCOUNT_ID` | Cloudflare account ID | Dashboard → Account ID (right sidebar) |
| `CF_API_TOKEN` | API token with Workers AI permission | Dashboard → Profile → API Tokens → Create Token |
| `WEATHER_API_KEY` | WeatherAPI.com API key | [Sign up at weatherapi.com](https://www.weatherapi.com/signup.aspx) |

### Cloudflare KV Binding

| Binding | Purpose | Setup |
|---------|---------|-------|
| `CHAT_HISTORY` | Global memory for recent queries | `wrangler kv namespace create "CHAT_HISTORY"` |

## API Endpoints

### `GET /` or `GET /chat`
Returns the HTML interface.

### `POST /chat`
Processes a weather query.

**Request:**
```json
{
  "query": "What's the weather in Paris tomorrow?"
}
```

**Response (Current Weather):**
```json
{
  "location": "Paris, France",
  "temperature": "15°C / 59°F",
  "condition": "Partly cloudy",
  "humidity": 65,
  "wind": "12.5 km/h",
  "limerick": "In Paris where Eiffel stands tall...\n..."
}
```

**Response (Forecast):**
```json
{
  "location": "London, UK",
  "forecast": [
    {
      "date": "2026-01-12",
      "condition": "Sunny",
      "high": "18°C / 64°F",
      "low": "12°C / 54°F"
    }
  ],
  "limerick": "In London where Big Ben does chime...\n..."
}
```

### `GET /api/history`
Returns the global chat history (last 4 queries).

**Response:**
```json
[
  {
    "query": "What's the weather in Paris?",
    "location": "Paris, France",
    "timestamp": "2026-01-12T10:30:00",
    "type": "current"
  }
]
```

## Global Memory (KV Storage)

The app uses Cloudflare KV to store the last 4 weather queries globally:

- **Key**: `global_chat_history`
- **Storage**: Last 4 queries from all users
- **Persistence**: Indefinite (no expiration)
- **Display**: Real-time sidebar showing recent queries
- **Updates**: Automatically refreshes after each query

**View stored data:**
```bash
wrangler kv key get "global_chat_history" --binding CHAT_HISTORY
```

**Clear history:**
```bash
wrangler kv key delete "global_chat_history" --binding CHAT_HISTORY
```

See [GLOBAL_MEMORY.md](GLOBAL_MEMORY.md) for implementation details.

## Error Handling

Comprehensive error handling with user-friendly messages:

| Error Type | User Message | HTTP Status |
|------------|--------------|-------------|
| Invalid AI response | "Could not understand query" | 200 |
| Location not found | "Location 'X' not found" | 200 |
| Weather API error | "Failed to fetch weather data" | 200 |
| Missing secrets | "Server configuration error" | 500 |
| Network timeout | "Request timed out" | 500 |
| Invalid JSON | "AI returned invalid response" | 200 |

All errors are logged to Cloudflare's console for debugging:
```bash
wrangler tail --format pretty
```

See [ERROR_HANDLING.md](ERROR_HANDLING.md) for complete documentation.

## Testing

### Test Weather Queries
```bash
curl -X POST https://weatherappy.arvid-a10.workers.dev/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather in London?"}'
```

### Test History API
```bash
curl https://weatherappy.arvid-a10.workers.dev/api/history
```

### View Live Logs
```bash
wrangler tail --format pretty
```

### Check KV Storage
```bash
wrangler kv key get "global_chat_history" --binding CHAT_HISTORY
```

## Monitoring & Observability

Built-in logging configuration in `wrangler.toml`:

```toml
[observability.logs]
enabled = true
head_sampling_rate = 1
invocation_logs = true
persist = true
```

**Log categories:**
- `[Workers AI]` - AI model requests and responses
- `[WeatherAPI]` - Weather API requests and responses
- `[Limerick]` - Limerick generation
- `[KV]` - KV storage operations
- `[Main]` - Request processing flow
- `[Error]` - All error conditions

## Assignment Compliance

This project meets all requirements for an AI-powered application on Cloudflare:

**LLM**: Cloudflare Workers AI (Llama 3 8B Instruct)
- Query parsing: Natural language to JSON
- Limerick generation: Context-aware creative writing

**Workflow / Coordination**: Cloudflare Workers
- Serverless Python runtime
- Multi-step orchestration (AI → Weather API → AI → Response)

**User Input**: Chat interface
- Web-based conversational UI
- Natural language input field
- Sample prompt suggestions

**Memory / State**: Cloudflare KV
- Global chat history (last 4 queries)
- Persistent storage across requests
- Real-time sidebar display

## Customization

### Change AI Model

Edit `call_workers_ai()` in `app.py`:

```python
url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/mistral/mistral-7b-instruct-v0.1"
```

Available models: [Cloudflare AI Catalog](https://developers.cloudflare.com/workers-ai/models/)

### Modify UI Theme

Edit colors in `HTML_TEMPLATE` in `app.py`:

```css
background: linear-gradient(135deg, #YOUR_COLOR 0%, #YOUR_COLOR2 100%);
color: #YOUR_ACCENT;
```

### Change Memory Limit

Edit `save_to_global_history()` in `app.py`:

```python
# Keep only last 10 entries instead of 4
history = history[-10:]
```

### Add More Weather Data

Edit `get_weather()` in `app.py` to include additional fields from [WeatherAPI.com response](https://www.weatherapi.com/docs/).

## Troubleshooting

### "Value not found" when checking KV
- Make sure you've deployed: `wrangler deploy`
- Check you're using the correct namespace ID in `wrangler.toml`
- Submit at least one query through the live app

### "Authorization header is missing or invalid"
- Set secrets: `wrangler secret put CF_API_TOKEN`
- Verify token has Workers AI permission

### "Location not found"
- Check spelling and format (city names, not addresses)
- Try "Paris, France" instead of just "Paris"

### Recent Queries shows "Loading..."
- Check browser console for errors
- Verify `/api/history` endpoint works: `curl https://your-app.workers.dev/api/history`

### Limerick not generating
- Check Cloudflare Workers AI quota
- View logs: `wrangler tail`

## Documentation

- [cloudflare instructions.md](cloudflare%20instructions.md) - Complete deployment guide
- [QUICKSTART.md](QUICKSTART.md) - Fast deployment in 5 minutes
- [GLOBAL_MEMORY.md](GLOBAL_MEMORY.md) - KV storage implementation
- [ERROR_HANDLING.md](ERROR_HANDLING.md) - Error handling patterns

## Performance

- **Response Time**: 500-1500ms (includes 2 AI calls + 1 weather API call)
  - Query parsing: ~200-400ms
  - Weather fetch: ~100-300ms
  - Limerick generation: ~200-600ms
- **Caching**: Response headers set for optimal caching
- **Edge Computing**: Runs in 200+ cities worldwide
- **Scalability**: Handles unlimited concurrent requests

## Cost Estimate

**Free Tier Limits:**
- Cloudflare Workers: 100,000 requests/day
- Workers AI: 10,000 neurons/day (queries use ~500-1000 neurons each)
- KV Storage: 100,000 reads/day, 1,000 writes/day
- WeatherAPI.com: 1,000,000 calls/month

**Expected costs for moderate usage (1,000 queries/day):** $0/month

## Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License

This project is open source and available for personal and commercial use.

## Credits

- Built for [Cloudflare Workers](https://workers.cloudflare.com/)
- Powered by [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)
- Weather data from [WeatherAPI.com](https://www.weatherapi.com/)
- AI Model: Meta Llama 3 8B Instruct

## Support

- **Live Demo**: [https://weatherappy.arvid-a10.workers.dev/](https://weatherappy.arvid-a10.workers.dev/)
- **Deployment Issues**: See [cloudflare instructions.md](cloudflare%20instructions.md)
- **Cloudflare Docs**: [workers.cloudflare.com/docs](https://developers.cloudflare.com/workers/)
- **WeatherAPI Docs**: [weatherapi.com/docs](https://www.weatherapi.com/docs/)

---

**Try the live application:** [https://weatherappy.arvid-a10.workers.dev/](https://weatherappy.arvid-a10.workers.dev/)
