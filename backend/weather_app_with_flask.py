from flask import Flask, jsonify
import requests
import datetime as dt
import random
import pytz
import backend.logger_configuration as logger_configuration

logger = logger_configuration.logger

app = Flask(__name__)

# Weather App Logic
api_key = "0060cf5abb2bfda0140d4fc62051bb9e"

city_list = [
    "New York", "Los Angeles", "Toronto", "Mexico City", "London", "Paris", "Berlin",
    "Madrid", "Prague", "Tokyo", "Beijing", "Mumbai", "Bangkok", "Singapore", "Sydney",
    "Melbourne", "Auckland", "Cairo", "Lagos", "Nairobi", "Cape Town"
]

city_timezones = {
    "New York": "America/New_York", "Los Angeles": "America/Los_Angeles",
    "Toronto": "America/Toronto", "Mexico City": "America/Mexico_City",
    "London": "Europe/London", "Paris": "Europe/Paris", "Berlin": "Europe/Berlin",
    "Madrid": "Europe/Madrid", "Prague": "Europe/Prague", "Tokyo": "Asia/Tokyo",
    "Beijing": "Asia/Shanghai", "Mumbai": "Asia/Kolkata", "Bangkok": "Asia/Bangkok",
    "Singapore": "Asia/Singapore", "Sydney": "Australia/Sydney", "Melbourne": "Australia/Melbourne",
    "Auckland": "Pacific/Auckland", "Cairo": "Africa/Cairo", "Lagos": "Africa/Lagos",
    "Nairobi": "Africa/Nairobi", "Cape Town": "Africa/Johannesburg"
}

def temp_kelvin_to_celsium(kelvin):
    celsium = kelvin - 273.15
    fahrenheit = celsium * 9/5 + 32
    return celsium, fahrenheit

def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url).json()
        logger.info("API request successful.")
        return response
    except Exception as e:
        logger.error("Failed to make API request: %s", e)
        return None

def get_weather_for_city(city):
    """Funkce, která připraví JSON pro frontend"""
    response = fetch_weather_data(city)
    if not response:
        return None

    try:
        temp_kelvin = response["main"]["temp"]
        temp_c, temp_f = temp_kelvin_to_celsium(temp_kelvin)
        feels_kelvin = response["main"]["feels_like"]
        feels_c, feels_f = temp_kelvin_to_celsium(feels_kelvin)
        wind_speed = response["wind"]["speed"]
        humidity = response["main"]["humidity"]
        description = response["weather"][0]["description"]

        return {
            "city": city,
            "temp_c": temp_c,
            "temp_f": temp_f,
            "feels_c": feels_c,
            "feels_f": feels_f,
            "wind": wind_speed,
            "humidity": humidity,
            "description": description
        }
    except KeyError as e:
        logger.error("Failed to retrieve data from response: %s", e)
        return None

@app.route("/weather")
def weather_endpoint():
    city = random.choice(city_list)
    data = get_weather_for_city(city)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500

if __name__ == "__main__":
    app.run(debug=True)