import requests
import json

def get_weather():
    """
    Get current weather using wttr.in (no API key required).
    Returns a formatted weather string.
    """
    try:
        # wttr.in is a free weather service that doesn't require API keys
        # It automatically detects location from IP
        response = requests.get(
            "https://wttr.in/?format=j1",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            temp_f = current['temp_F']
            temp_c = current['temp_C']
            condition = current['weatherDesc'][0]['value']
            feels_like_f = current['FeelsLikeF']
            humidity = current['humidity']
            
            # Get location
            location = data['nearest_area'][0]
            city = location['areaName'][0]['value']
            region = location.get('region', [{}])[0].get('value', '')
            
            weather_report = (
                f"The temperature in {city} is {temp_f}°F ({temp_c}°C), "
                f"feels like {feels_like_f}°F. "
                f"Conditions: {condition}. "
                f"Humidity: {humidity}%."
            )
            
            return weather_report
        else:
            return "I couldn't fetch the weather information right now."
            
    except Exception as e:
        print(f"Weather API error: {e}")
        return "I encountered an error getting the weather."
