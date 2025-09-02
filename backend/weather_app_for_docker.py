import requests
import datetime as dt
import random
import pytz
import logger_configuration

# Import logger from logger_configuration
logger = logger_configuration.logger

def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url).json()
        logger.info("API request successful.")
        return response
    except Exception as e:
        logger.error("Failed to make API request: %s", e)
        return None

def display_weather_info(response, city):
    try:
        temp_kelvin = response["main"]["temp"]
        temp_celsium, temp_fahrenheit = temp_kelvin_to_celsium(temp_kelvin)
        feeling_like_kelvin = response["main"]["feels_like"]
        feeling_like_celsium, feeling_like_fahrenheit = temp_kelvin_to_celsium(feeling_like_kelvin)
        wind_speed = response["wind"]["speed"]
        humidity = response["main"]["humidity"]
        description = response["weather"][0]["description"]
        sunrise_time = dt.datetime.fromtimestamp(response["sys"]["sunrise"] + response["timezone"], dt.timezone.utc)
        sunset_time = dt.datetime.fromtimestamp(response["sys"]["sunset"] + response["timezone"], dt.timezone.utc)

        czech_tz = pytz.timezone('Europe/Prague')
        city_tz = pytz.timezone(city_timezones[city])
        current_time_in_city = dt.datetime.now(city_tz).strftime('%H:%M:%S')
        current_time_in_czech = dt.datetime.now(czech_tz).strftime('%H:%M:%S')

        print(f"Name of the city: {city}")
        print(f"Current time in {city}: {current_time_in_city} local time")
        print(f"Temperature in {city}: {temp_celsium:.2f}°C or {temp_fahrenheit:.2f}°F")
        print(f"Temperature in {city} feels like: {feeling_like_celsium:.2f}°C or {feeling_like_fahrenheit:.2f}°F")
        print(f"General weather in {city}: {description}")
        print(f"Sunrise in {city}: {sunrise_time} local time")
        print(f"Sunset in {city}: {sunset_time} local time")
        print(f"Wind speed in {city}: {wind_speed} m/s")
        print(f"Humidity in {city}: {humidity}%")
        print(f"Time in the {city} is {current_time_in_city} and time in the Czech Republic is {current_time_in_czech}")
        
        logger.info("Weather data displayed successfully.")
    except KeyError as e:
        logger.error("Failed to retrieve data from response: %s", e)

def main():
    logger.info("Script execution started")
    
    city = random.choice(city_list)  # Select a random city from the list
    logger.info(f"Selected city: {city}")
    
    response = fetch_weather_data(city)  # Fetch weather data for the selected city
    
    if response:
        display_weather_info(response, city)  # Display the weather information
        logger.info("All processes completed successfully - Everything OK.")
    else:
        logger.critical("Failed to fetch weather data for the city: %s", city)
    
    logger.info("Script execution ended")

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

if __name__ == "__main__":
    main()