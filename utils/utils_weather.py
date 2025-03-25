import requests


def fetch_weather_info(api_key: str, city: str):
    """Fetches weather conditions for a given city from OpenWeatherMap API."""
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Fetch temperature in Celsius
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "coordinates": {
                "latitude": data["coord"]["lat"],
                "longitude": data["coord"]["lon"]
            }
        }
        return weather_info
    else:
        return {"error": f"Failed to fetch data: {response.status_code}"}

def get_weather_info(api_key: str, city: str):
    """Fetches and formats weather conditions into a readable string."""
    weather = fetch_weather_info(api_key, city)
    if "error" in weather:
        return weather["error"]
    
    return (f"Weather Report for {city.capitalize()}\n"
            f"Description: {weather['description'].capitalize()}\n"
            f"Temperature: {weather['temperature']}°C\n"
            f"Wind Speed: {weather['wind_speed']} m/s\n"
            f"Pressure: {weather['pressure']} hPa\n"
            f"Humidity: {weather['humidity']}%\n"
            f"Coordinates: ({weather['coordinates']['latitude']}, {weather['coordinates']['longitude']})")
