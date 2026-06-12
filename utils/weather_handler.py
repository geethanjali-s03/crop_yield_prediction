"""
Weather & Location Handler
Integrates with free weather and geolocation APIs
"""
import requests
import json
from datetime import datetime
from config import Config

def get_weather_data(latitude, longitude):
    """
    Fetch weather data from Open-Meteo API (Free)
    Returns: {temperature, humidity, rainfall, wind_speed, weather_code}
    """
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,precipitation",
            "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,rain_sum",
            "timezone": "auto"
        }
        response = requests.get(Config.WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data.get('current', {})
        
        return {
            'status': 'success',
            'temperature': current.get('temperature_2m', 0),
            'humidity': current.get('relative_humidity_2m', 0),
            'rainfall': current.get('precipitation', 0),
            'wind_speed': current.get('wind_speed_10m', 0),
            'weather_code': current.get('weather_code', 0),
            'timestamp': datetime.now().isoformat(),
            'location': {'latitude': latitude, 'longitude': longitude}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'temperature': 0,
            'humidity': 0,
            'rainfall': 0,
            'wind_speed': 0
        }

def get_weather_forecast(latitude, longitude, days=7):
    """
    Fetch weather forecast for specified days
    Returns: List of daily forecasts
    """
    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,rain_sum,precipitation_sum",
            "timezone": "auto"
        }
        response = requests.get(Config.WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        daily = data.get('daily', {})
        
        forecasts = []
        for i in range(min(days, len(daily.get('time', [])))):
            forecasts.append({
                'date': daily['time'][i],
                'max_temp': daily['temperature_2m_max'][i],
                'min_temp': daily['temperature_2m_min'][i],
                'rainfall': daily['rain_sum'][i],
                'weather_code': daily['weather_code'][i]
            })
        
        return {
            'status': 'success',
            'forecast': forecasts,
            'location': {'latitude': latitude, 'longitude': longitude}
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'forecast': []
        }

def interpret_weather_code(code):
    """Convert WMO weather code to readable description"""
    weather_codes = {
        0: 'Clear Sky',
        1: 'Mainly Clear',
        2: 'Partly Cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Depositing Rime Fog',
        51: 'Light Drizzle',
        53: 'Moderate Drizzle',
        55: 'Dense Drizzle',
        61: 'Slight Rain',
        63: 'Moderate Rain',
        65: 'Heavy Rain',
        71: 'Slight Snow',
        73: 'Moderate Snow',
        75: 'Heavy Snow',
        77: 'Snow Grains',
        80: 'Slight Rain Showers',
        81: 'Moderate Rain Showers',
        82: 'Violent Rain Showers',
        85: 'Slight Snow Showers',
        86: 'Heavy Snow Showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with Slight Hail',
        99: 'Thunderstorm with Heavy Hail'
    }
    return weather_codes.get(code, 'Unknown')

def get_location_from_ip():
    """Get approximate user location from IP (Free geolocation)"""
    try:
        # Using ipapi.co (Free tier, no key required)
        response = requests.get('https://ipapi.co/json/', timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return {
            'status': 'success',
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country_name')
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def get_location_from_name(city_name, state=None):
    """Get coordinates from city name using Nominatim (Free)"""
    try:
        query = f"{city_name}, {state}, India" if state else f"{city_name}, India"
        response = requests.get(
            'https://nominatim.openstreetmap.org/search',
            params={'q': query, 'format': 'json'},
            timeout=10,
            headers={'User-Agent': 'CropYieldAI/1.0'}
        )
        response.raise_for_status()
        
        results = response.json()
        if results:
            result = results[0]
            return {
                'status': 'success',
                'latitude': float(result['lat']),
                'longitude': float(result['lon']),
                'display_name': result['display_name']
            }
        else:
            return {'status': 'error', 'message': 'Location not found'}
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def validate_coordinates(latitude, longitude):
    """Validate latitude and longitude"""
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True, lat, lon
        else:
            return False, None, None
    except:
        return False, None, None

def get_suitable_crops_for_weather(weather_data):
    """
    Suggest crops based on current weather conditions
    """
    temperature = weather_data.get('temperature', 20)
    humidity = weather_data.get('humidity', 50)
    rainfall = weather_data.get('rainfall', 0)
    
    suitable_crops = []
    
    # Rice: Prefers warm, wet conditions
    if 25 <= temperature <= 35 and humidity > 60 and rainfall > 0:
        suitable_crops.append({'crop': 'Rice', 'suitability': 0.9})
    
    # Wheat: Prefers cool season
    if 15 <= temperature <= 25 and humidity > 40:
        suitable_crops.append({'crop': 'Wheat', 'suitability': 0.85})
    
    # Maize: Moderate temperature
    if 20 <= temperature <= 30 and humidity > 50:
        suitable_crops.append({'crop': 'Maize', 'suitability': 0.8})
    
    # Sugarcane: Warm, wet
    if 22 <= temperature <= 32 and humidity > 50:
        suitable_crops.append({'crop': 'Sugarcane', 'suitability': 0.75})
    
    # Cotton: Warm, moderate rainfall
    if 21 <= temperature <= 32 and 40 <= humidity <= 70:
        suitable_crops.append({'crop': 'Cotton', 'suitability': 0.7})
    
    return sorted(suitable_crops, key=lambda x: x['suitability'], reverse=True)
