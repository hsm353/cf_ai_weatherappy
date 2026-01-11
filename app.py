import os
import json
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


def call_workers_ai(prompt, account_id, api_token):
    """
    Call Cloudflare Workers AI to convert natural language to JSON structure
    """
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3-8b-instruct"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are a weather query parser. Convert natural language weather queries into JSON.
Output format: {"intent": "get_weather", "q": "location", "units": "metric"|"imperial", "timeframe": "now"|"today"|"tomorrow"|"7d"}

Rules:
- Default to "metric" unless Fahrenheit/imperial is mentioned
- Default to "now" unless a specific timeframe is mentioned
- For "tomorrow", use timeframe "tomorrow"
- For "week" or "7 days", use timeframe "7d"
- Extract the location name for "q"
- Output ONLY valid JSON, no other text
- The location should be just the city name or "city, country"

Examples:
Input: "What's the weather in Paris?"
Output: {"intent": "get_weather", "q": "Paris", "units": "metric", "timeframe": "now"}

Input: "Weather in New York tomorrow in Fahrenheit"
Output: {"intent": "get_weather", "q": "New York", "units": "imperial", "timeframe": "tomorrow"}

Input: "7 day forecast for London"
Output: {"intent": "get_weather", "q": "London", "units": "metric", "timeframe": "7d"}"""
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # Extract the AI response
        if result.get("success") and result.get("result"):
            ai_response = result["result"]["response"]
            return ai_response
        else:
            return None
    except Exception as e:
        print(f"Error calling Workers AI: {e}")
        return None


def get_weather(query_params, api_key):
    """
    Call weather.com API (OpenWeatherMap as example) to get weather data
    """
    # Using OpenWeatherMap API as a common weather API
    # You can replace this with weather.com's actual API
    base_url = "https://api.openweathermap.org/data/2.5/"
    
    location = query_params.get("q", "")
    units = query_params.get("units", "metric")
    timeframe = query_params.get("timeframe", "now")
    
    if not location:
        return {"error": "No location specified"}
    
    try:
        if timeframe in ["now", "today"]:
            # Current weather
            url = f"{base_url}weather"
            params = {
                "q": location,
                "units": units,
                "appid": api_key
            }
        else:
            # Forecast weather
            url = f"{base_url}forecast"
            params = {
                "q": location,
                "units": units,
                "appid": api_key
            }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Format the response
        if timeframe in ["now", "today"]:
            temp_unit = "°F" if units == "imperial" else "°C"
            wind_unit = "mph" if units == "imperial" else "m/s"
            
            return {
                "location": f"{data['name']}, {data['sys']['country']}",
                "temperature": f"{data['main']['temp']}{temp_unit}",
                "condition": data['weather'][0]['description'].title(),
                "humidity": data['main']['humidity'],
                "wind": f"{data['wind']['speed']} {wind_unit}"
            }
        else:
            # Forecast data
            temp_unit = "°F" if units == "imperial" else "°C"
            forecast_list = []
            
            # Get daily forecasts (every 8th item is roughly 24 hours)
            for i in range(0, min(len(data['list']), 40), 8):
                item = data['list'][i]
                forecast_list.append({
                    "date": item['dt_txt'].split()[0],
                    "condition": item['weather'][0]['description'].title(),
                    "high": f"{item['main']['temp_max']}{temp_unit}",
                    "low": f"{item['main']['temp_min']}{temp_unit}"
                })
            
            return {
                "location": f"{data['city']['name']}, {data['city']['country']}",
                "forecast": forecast_list[:7] if timeframe == "7d" else forecast_list[:2]
            }
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"Location '{location}' not found"}
        else:
            return {"error": f"Weather API error: {e}"}
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}


def generate_limerick(location, weather_condition, temperature, account_id, api_token):
    """
    Generate a limerick about the city and its weather using Cloudflare Workers AI
    """
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3-8b-instruct"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Write a fun, creative limerick (5-line poem with AABBA rhyme scheme) about {location} and its current weather.

Weather details:
- Location: {location}
- Condition: {weather_condition}
- Temperature: {temperature}

The limerick should be playful and weather-themed. Output ONLY the limerick, no other text."""
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a creative poet who writes fun limericks. Output only the limerick poem, nothing else."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("success") and result.get("result"):
            limerick = result["result"]["response"].strip()
            # Remove any quotes or extra formatting
            limerick = limerick.strip('"').strip("'")
            return limerick
        else:
            return None
    except Exception as e:
        print(f"Error generating limerick: {e}")
        return None


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        # Return the HTML interface
        return render_template('chat.html')
    
    elif request.method == 'POST':
        # Process the user query
        data = request.get_json()
        user_query = data.get('query', '').strip()
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Get environment variables
        cf_account_id = os.environ.get('CF_ACCOUNT_ID')
        cf_api_token = os.environ.get('CF_API_TOKEN')
        weather_api_key = os.environ.get('WEATHER_API_KEY')
        
        if not all([cf_account_id, cf_api_token, weather_api_key]):
            return jsonify({"error": "Missing required environment variables"}), 500
        
        # Call Workers AI to parse the query
        ai_response = call_workers_ai(user_query, cf_account_id, cf_api_token)
        
        if not ai_response:
            return jsonify({"error": "Did not work! AI service unavailable."}), 500
        
        # Try to parse the AI response as JSON
        try:
            # Extract JSON from the response (sometimes AI adds extra text)
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                return jsonify({"error": "Did not work! Invalid AI response format."}), 500
            
            json_str = ai_response[json_start:json_end]
            query_params = json.loads(json_str)
            
            # Validate the JSON structure
            if query_params.get("intent") != "get_weather" or "q" not in query_params:
                return jsonify({"error": "Did not work! Invalid query structure."}), 500
            
        except json.JSONDecodeError:
            return jsonify({"error": "Did not work! Could not parse AI response as JSON."}), 500
        except Exception as e:
            return jsonify({"error": f"Did not work! Error: {str(e)}"}), 500
        
        # Get weather data
        weather_data = get_weather(query_params, weather_api_key)
        
        if "error" in weather_data:
            return jsonify(weather_data), 400
        
        # Generate a limerick about the city and weather
        location = weather_data.get('location', query_params.get('q', 'Unknown'))
        condition = weather_data.get('condition', 'unknown weather')
        temperature = weather_data.get('temperature', 'unknown temperature')
        
        limerick = generate_limerick(location, condition, temperature, cf_account_id, cf_api_token)
        
        # Add limerick to response (or null if generation failed)
        weather_data['limerick'] = limerick
        
        return jsonify(weather_data), 200


@app.route('/')
def index():
    # Redirect to chat
    return chat()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8787)
