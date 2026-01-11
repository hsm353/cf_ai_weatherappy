# Migration to WeatherAPI.com 🌤️

## What Changed?

The weather data provider has been changed from OpenWeatherMap to WeatherAPI.com.

## Why WeatherAPI.com?

### Benefits

✅ **Generous Free Tier**
- 1,000,000 calls/month (vs OpenWeatherMap's 1,000/day)
- No rate limiting on free tier
- No credit card required

✅ **Better API Design**
- Simpler, more intuitive endpoints
- Consistent response format
- Better documentation
- Faster response times

✅ **More Features**
- Current weather
- 3-day forecast (14-day on paid)
- Historical weather
- Astronomy data
- Air quality index
- Better location search

✅ **Reliability**
- 99.9% uptime SLA
- Multiple data centers
- Fast CDN delivery
- Real-time updates

## API Comparison

### OpenWeatherMap (Old)
```
Base URL: https://api.openweathermap.org/data/2.5/
Current: /weather?q=London&appid=KEY&units=metric
Forecast: /forecast?q=London&appid=KEY&units=metric

Free Tier: 60 calls/min, 1,000 calls/day
```

### WeatherAPI.com (New)
```
Base URL: http://api.weatherapi.com/v1/
Current: /current.json?key=KEY&q=London
Forecast: /forecast.json?key=KEY&q=London&days=7

Free Tier: 1,000,000 calls/month (no rate limit)
```

## Code Changes

### Function Signature (Unchanged)
```python
async def get_weather(query_params, api_key):
```

### API Endpoints
```python
# OLD (OpenWeatherMap)
base_url = "https://api.openweathermap.org/data/2.5/"
url = f"{base_url}weather?q={location}&units={units}&appid={api_key}"

# NEW (WeatherAPI.com)
base_url = "http://api.weatherapi.com/v1/"
url = f"{base_url}current.json?key={api_key}&q={location}"
```

### Response Format

**Temperature:**
```python
# OLD
temp = data['main']['temp']
condition = data['weather'][0]['description']

# NEW
temp = data['current']['temp_c']  # or temp_f
condition = data['current']['condition']['text']
```

**Location:**
```python
# OLD
location = f"{data['name']}, {data['sys']['country']}"

# NEW
location = f"{data['location']['name']}, {data['location']['country']}"
```

**Wind Speed:**
```python
# OLD
wind = data['wind']['speed']  # always m/s

# NEW
wind = data['current']['wind_kph']  # or wind_mph
```

### Units Handling

**OLD (OpenWeatherMap):**
- API accepts `units` parameter (metric/imperial)
- Single API call for either unit

**NEW (WeatherAPI.com):**
- API returns both units in response
- Choose appropriate field: `temp_c` or `temp_f`
- More flexible, no need for separate API calls

## Migration Steps

### 1. Get WeatherAPI.com API Key

```bash
# Visit https://www.weatherapi.com/signup.aspx
# Sign up for free account
# Copy API key from dashboard
```

### 2. Update Cloudflare Secrets

```bash
# Update the WEATHER_API_KEY secret
wrangler secret put WEATHER_API_KEY
# Paste your new WeatherAPI.com key
```

### 3. Deploy Updated Code

```bash
wrangler deploy
```

That's it! No other changes needed.

## Testing the Migration

### Test Current Weather
```
Query: "What's the weather in London?"

Expected Response:
- Location: "London, United Kingdom"
- Temperature: "15°C" (or °F if imperial)
- Condition: "Partly cloudy"
- Humidity: 65%
- Wind: "15 kph" (or mph if imperial)
- Limerick: AI-generated poem
```

### Test Forecast
```
Query: "7 day forecast for Paris"

Expected Response:
- Location: "Paris, France"
- Forecast array with 7 days
- Each day has: date, condition, high, low
- Plus AI-generated limerick
```

### Test Units
```
Query: "Weather in New York in Fahrenheit"

Expected Response:
- Temperature in °F
- Wind in mph
- Everything else same format
```

## Error Handling

### Location Not Found
```json
{
  "error": "Location 'Xyz' not found"
}
```

### API Key Invalid
```json
{
  "error": "Weather API error: HTTP 401"
}
```

### API Quota Exceeded
```json
{
  "error": "Weather API error: HTTP 429"
}
```

## API Response Examples

### Current Weather
```json
{
  "location": {
    "name": "London",
    "country": "United Kingdom"
  },
  "current": {
    "temp_c": 15.0,
    "temp_f": 59.0,
    "condition": {
      "text": "Partly cloudy"
    },
    "wind_kph": 15.0,
    "wind_mph": 9.3,
    "humidity": 65
  }
}
```

### Forecast
```json
{
  "location": {
    "name": "Paris",
    "country": "France"
  },
  "forecast": {
    "forecastday": [
      {
        "date": "2026-01-11",
        "day": {
          "maxtemp_c": 18.0,
          "maxtemp_f": 64.4,
          "mintemp_c": 12.0,
          "mintemp_f": 53.6,
          "condition": {
            "text": "Sunny"
          }
        }
      }
    ]
  }
}
```

## Cost Comparison

### OpenWeatherMap Free Tier
- 1,000 calls/day = ~30,000 calls/month
- 60 calls/minute rate limit
- Need credit card for higher tiers

### WeatherAPI.com Free Tier
- **1,000,000 calls/month**
- No rate limit
- No credit card required

**Result:** 33x more API calls available!

## Backward Compatibility

### User Experience
✅ **No changes** to user interface
✅ **Same queries** work identically
✅ **Same response format** to frontend
✅ **Same features** (current + forecast)

### Developer Experience
✅ **Same environment variable** name (`WEATHER_API_KEY`)
✅ **Same function signatures** in code
✅ **Same error handling** patterns
✅ **Same deployment process**

## Troubleshooting

### Issue: Getting 401 Errors

**Solution:**
1. Check API key is valid at weatherapi.com
2. Verify secret is set: `wrangler secret list`
3. Update secret: `wrangler secret put WEATHER_API_KEY`
4. Redeploy: `wrangler deploy`

### Issue: Location Not Found

**Possible causes:**
- Typo in city name
- City name ambiguity (e.g., "Paris, Texas" vs "Paris, France")

**Solution:**
- Use full city name: "Paris, France"
- Or use latitude,longitude: "48.8566,2.3522"
- Or use zip code: "90210"

### Issue: Response Format Different

**Check:**
- Make sure you're using the latest deployed version
- Clear browser cache
- Check worker logs: `wrangler tail`

## Additional Features Available

WeatherAPI.com offers many more features you could add:

### Air Quality
```python
url = f"{base_url}current.json?key={api_key}&q={location}&aqi=yes"
# Response includes: aqi, pm2_5, pm10, etc.
```

### Astronomy
```python
url = f"{base_url}astronomy.json?key={api_key}&q={location}&dt={date}"
# Response includes: sunrise, sunset, moonrise, moonset, moon phase
```

### Historical Weather
```python
url = f"{base_url}history.json?key={api_key}&q={location}&dt=2026-01-01"
# Get weather data from past dates
```

### Alerts
```python
url = f"{base_url}forecast.json?key={api_key}&q={location}&alerts=yes"
# Get severe weather alerts
```

## Documentation Links

- **WeatherAPI.com Docs:** https://www.weatherapi.com/docs/
- **API Explorer:** https://www.weatherapi.com/api-explorer.aspx
- **Pricing:** https://www.weatherapi.com/pricing.aspx
- **Status Page:** https://www.weatherapi.com/api-status.aspx

## Support

### WeatherAPI.com Support
- Email: support@weatherapi.com
- Forum: community.weatherapi.com

### This Project
- Check [cloudflare instructions.md](cloudflare%20instructions.md)
- Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Migration Date:** January 2026  
**Migration Status:** ✅ Complete  
**Impact:** Positive (better API, more features, higher limits)

**Happy weather forecasting! 🌤️**
