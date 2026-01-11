from js import Response, fetch, Object, Headers
import json

# HTML template for the chat interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Chat App</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            padding: 30px;
        }
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 20px;
            font-size: 2em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .chat-box {
            background: #f7f7f7;
            border-radius: 15px;
            padding: 20px;
            min-height: 200px;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .message {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .weather-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        .weather-item {
            background: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
        .limerick {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-top: 15px;
            border-radius: 8px;
            font-style: italic;
            white-space: pre-line;
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: scale(1.05);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .error {
            background: #ffe6e6;
            border-left: 4px solid #ff4444;
            padding: 15px;
            border-radius: 8px;
            color: #cc0000;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather Chat</h1>
        <p class="subtitle">Ask me about the weather anywhere!</p>
        
        <div class="chat-box" id="chatBox"></div>
        
        <div class="input-group">
            <input type="text" id="queryInput" placeholder="What's the weather in Paris?" />
            <button onclick="sendQuery()" id="sendBtn">Send</button>
        </div>
    </div>

    <script>
        async function sendQuery() {
            const input = document.getElementById('queryInput');
            const query = input.value.trim();
            if (!query) return;

            const chatBox = document.getElementById('chatBox');
            const sendBtn = document.getElementById('sendBtn');
            
            // Disable input
            sendBtn.disabled = true;
            input.disabled = true;
            
            // Show loading
            chatBox.innerHTML += '<div class="loading">🔄 Fetching weather...</div>';
            chatBox.scrollTop = chatBox.scrollHeight;
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                
                // Remove loading
                const loadingDiv = chatBox.querySelector('.loading');
                if (loadingDiv) loadingDiv.remove();
                
                // Display result
                let html = '<div class="message">';
                
                if (data.error) {
                    html += `<div class="error">${data.error}</div>`;
                } else {
                    html += `<h3>📍 ${data.location}</h3>`;
                    html += '<div class="weather-info">';
                    html += `<div class="weather-item"><strong>🌡️ Temp</strong><br>${data.temperature}</div>`;
                    html += `<div class="weather-item"><strong>☁️ Condition</strong><br>${data.condition}</div>`;
                    html += `<div class="weather-item"><strong>💧 Humidity</strong><br>${data.humidity}%</div>`;
                    html += `<div class="weather-item"><strong>💨 Wind</strong><br>${data.wind}</div>`;
                    html += '</div>';
                    
                    if (data.limerick) {
                        html += `<div class="limerick">📝 ${data.limerick}</div>`;
                    }
                }
                
                html += '</div>';
                chatBox.innerHTML += html;
                chatBox.scrollTop = chatBox.scrollHeight;
                
                // Clear input
                input.value = '';
                
            } catch (error) {
                const loadingDiv = chatBox.querySelector('.loading');
                if (loadingDiv) loadingDiv.remove();
                chatBox.innerHTML += `<div class="message"><div class="error">Failed to fetch weather: ${error.message}</div></div>`;
            } finally {
                sendBtn.disabled = false;
                input.disabled = false;
                input.focus();
            }
        }
        
        // Allow Enter key to send
        document.getElementById('queryInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendQuery();
        });
        
        // Focus input on load
        document.getElementById('queryInput').focus();
    </script>
</body>
</html>
"""


async def call_workers_ai(prompt, account_id, api_token):
    """Call Cloudflare Workers AI to convert natural language to JSON structure"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3-8b-instruct"
    
    system_prompt = """You are a weather query parser. Convert natural language weather queries into JSON.
Output format: {"intent": "get_weather", "q": "location", "units": "metric"|"imperial", "timeframe": "now"|"today"|"tomorrow"|"7d"}

Rules:
- Default to "metric" unless Fahrenheit/imperial is mentioned
- Default to "now" unless a specific timeframe is mentioned
- Extract the location name for "q"
- Output ONLY valid JSON, no other text

Examples:
Input: "What's the weather in Paris?"
Output: {"intent": "get_weather", "q": "Paris", "units": "metric", "timeframe": "now"}"""
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    
    headers = Headers.new()
    headers.set("Authorization", f"Bearer {api_token}")
    headers.set("Content-Type", "application/json")
    
    response = await fetch(url, method="POST", headers=headers, body=json.dumps(payload))
    result = await response.json()
    
    if result.get("success") and result.get("result"):
        return result["result"]["response"]
    return None


async def get_weather(query_params, api_key):
    """Call WeatherAPI.com to get weather data"""
    base_url = "http://api.weatherapi.com/v1/"
    
    location = query_params.get("q", "")
    units = query_params.get("units", "metric")
    timeframe = query_params.get("timeframe", "now")
    
    if not location:
        return {"error": "No location specified"}
    
    try:
        # Determine endpoint and parameters based on timeframe
        if timeframe in ["now", "today"]:
            # Current weather
            url = f"{base_url}current.json?key={api_key}&q={location}"
        else:
            # Forecast weather (3-day forecast)
            days = 7 if timeframe == "7d" else 3
            url = f"{base_url}forecast.json?key={api_key}&q={location}&days={days}"
        
        # Log the request (without exposing full API key)
        masked_url = url.replace(api_key, f"{api_key[:8]}...{api_key[-4:]}")
        print(f"[WeatherAPI Request] URL: {masked_url}")
        print(f"[WeatherAPI Request] Location: {location}, Units: {units}, Timeframe: {timeframe}")
        
        response = await fetch(url)
        
        # Log the response status
        print(f"[WeatherAPI Response] Status: {response.status} {response.statusText if hasattr(response, 'statusText') else ''}")
        
        if not response.ok:
            if response.status == 400:
                print(f"[WeatherAPI Response] Error: Location '{location}' not found")
                return {"error": f"Location '{location}' not found"}
            print(f"[WeatherAPI Response] Error: HTTP {response.status}")
            return {"error": f"Weather API error: HTTP {response.status}"}
        
        data = await response.json()
        
        # Log the response data (truncated for readability)
        print(f"[WeatherAPI Response] Data received for: {data.get('location', {}).get('name', 'Unknown')}")
        if 'current' in data:
            print(f"[WeatherAPI Response] Current temp: {data['current'].get('temp_c')}°C / {data['current'].get('temp_f')}°F")
            print(f"[WeatherAPI Response] Condition: {data['current']['condition'].get('text', 'N/A')}")
        
        # Check for API error response
        if 'error' in data:
            error_msg = data['error'].get('message', 'Weather API error')
            print(f"[WeatherAPI Response] API Error: {error_msg}")
            return {"error": error_msg}
        
        # Determine temperature and wind units
        if units == "imperial":
            temp_unit = "°F"
            wind_unit = "mph"
            temp_value = data['current']['temp_f']
            wind_value = data['current']['wind_mph']
        else:
            temp_unit = "°C"
            wind_unit = "kph"
            temp_value = data['current']['temp_c']
            wind_value = data['current']['wind_kph']
        
        if timeframe in ["now", "today"]:
            # Current weather response
            return {
                "location": f"{data['location']['name']}, {data['location']['country']}",
                "temperature": f"{temp_value}{temp_unit}",
                "condition": data['current']['condition']['text'],
                "humidity": data['current']['humidity'],
                "wind": f"{wind_value} {wind_unit}"
            }
        else:
            # Forecast response
            forecast_list = []
            for day in data['forecast']['forecastday']:
                if units == "imperial":
                    high = f"{day['day']['maxtemp_f']}°F"
                    low = f"{day['day']['mintemp_f']}°F"
                else:
                    high = f"{day['day']['maxtemp_c']}°C"
                    low = f"{day['day']['mintemp_c']}°C"
                
                forecast_list.append({
                    "date": day['date'],
                    "condition": day['day']['condition']['text'],
                    "high": high,
                    "low": low
                })
            
            return {
                "location": f"{data['location']['name']}, {data['location']['country']}",
                "forecast": forecast_list
            }
    except Exception as e:
        print(f"[WeatherAPI Error] Exception occurred: {str(e)}")
        return {"error": f"Failed to fetch weather: {str(e)}"}


async def generate_limerick(location, weather_condition, temperature, account_id, api_token):
    """Generate a limerick about the city and its weather"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3-8b-instruct"
    
    prompt = f"""Write a fun, creative limerick (5-line poem with AABBA rhyme scheme) about {location} and its current weather.

Weather details:
- Location: {location}
- Condition: {weather_condition}
- Temperature: {temperature}

Output ONLY the limerick, no other text."""
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a creative poet who writes fun limericks. Output only the limerick poem, nothing else."},
            {"role": "user", "content": prompt}
        ]
    }
    
    headers = Headers.new()
    headers.set("Authorization", f"Bearer {api_token}")
    headers.set("Content-Type", "application/json")
    
    try:
        response = await fetch(url, method="POST", headers=headers, body=json.dumps(payload))
        result = await response.json()
        
        if result.get("success") and result.get("result"):
            limerick = result["result"]["response"].strip().strip('"').strip("'")
            return limerick
        return None
    except:
        return None


async def on_fetch(request, env):
    """Main fetch handler for Cloudflare Workers"""
    url = request.url
    method = request.method
    
    # Parse URL
    path = url.split('://')[1].split('/')[1:] if '://' in url else []
    path = '/' + '/'.join(path) if path else '/'
    
    # GET / or /chat - return HTML interface
    if method == "GET" and path in ['/', '/chat']:
        headers = Headers.new()
        headers.set("Content-Type", "text/html")
        return Response.new(HTML_TEMPLATE, status=200, headers=headers)
    
    # POST /chat - handle weather query
    elif method == "POST" and path == '/chat':
        try:
            body = await request.text()
            data = json.loads(body)
            user_query = data.get('query', '').strip()
            
            if not user_query:
                return Response.new(json.dumps({"error": "No query provided"}), status=400)
            
            # Get environment variables
            cf_account_id = env.CF_ACCOUNT_ID
            cf_api_token = env.CF_API_TOKEN
            weather_api_key = env.WEATHER_API_KEY
            
            if not all([cf_account_id, cf_api_token, weather_api_key]):
                return Response.new(json.dumps({"error": "Missing required environment variables"}), status=500)
            
            # Call Workers AI to parse the query
            ai_response = await call_workers_ai(user_query, cf_account_id, cf_api_token)
            
            if not ai_response:
                return Response.new(json.dumps({"error": "Did not work! AI service unavailable."}), status=500)
            
            # Parse AI response as JSON
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                return Response.new(json.dumps({"error": "Did not work! Invalid AI response format."}), status=500)
            
            json_str = ai_response[json_start:json_end]
            query_params = json.loads(json_str)
            
            if query_params.get("intent") != "get_weather" or "q" not in query_params:
                return Response.new(json.dumps({"error": "Did not work! Invalid query structure."}), status=500)
            
            # Get weather data
            weather_data = await get_weather(query_params, weather_api_key)
            
            if "error" in weather_data:
                return Response.new(json.dumps(weather_data), status=400)
            
            # Generate limerick
            location = weather_data.get('location', query_params.get('q', 'Unknown'))
            condition = weather_data.get('condition', 'unknown weather')
            temperature = weather_data.get('temperature', 'unknown temperature')
            
            limerick = await generate_limerick(location, condition, temperature, cf_account_id, cf_api_token)
            weather_data['limerick'] = limerick
            
            headers = Headers.new()
            headers.set("Content-Type", "application/json")
            return Response.new(json.dumps(weather_data), status=200, headers=headers)
            
        except Exception as e:
            return Response.new(json.dumps({"error": f"Did not work! Error: {str(e)}"}), status=500)
    
    # 404 for other routes
    return Response.new("Not Found", status=404)
