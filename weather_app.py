import requests
import datetime as dt
import json
import random
import pytz


base_url = "https://api.openweathermap.org/data/2.5/weather?"
api_key = "0060cf5abb2bfda0140d4fc62051bb9e"
city_list = [
    "London",
    "Paris",
    "Tokyo",
    "New York",
    "Sydney",
    "Beijing",
    "Rome",
    "Berlin",
    "Moscow",
    "Madrid"
]
city = random.choice(city_list)

city_timezones = {
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Tokyo": "Asia/Tokyo",
    "New York": "America/New_York",
    "Sydney": "Australia/Sydney",
    "Beijing": "Asia/Shanghai",
    "Rome": "Europe/Rome",
    "Berlin": "Europe/Berlin",
    "Moscow": "Europe/Moscow",
    "Madrid": "Europe/Madrid"
}

def temp_kelvin_to_celsium(kelvin):
    celsium = kelvin - 273.15
    fahrenheit = celsium * 9/5 + 32
    return celsium, fahrenheit

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

response = requests.get(url).json()



temp_kelvin = (response["main"]["temp"])
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
print(f"Description in {city}: {description}")
print(f"Temperature in {city}: {temp_celsium:.2f}°C or {temp_fahrenheit:.2f}°F")
print(f"Temperature in {city} feels like: {feeling_like_celsium:.2f}°C or {feeling_like_fahrenheit:.2f}°F")
print(f"General weather in {city}: {description}")
print(f"Sunrise in {city}: {sunrise_time} local time")
print(f"Sunset in {city}: {sunset_time} local time")
print(f"Wind speed in {city}: {wind_speed} m/s")
print(f"Humidity in {city}: {humidity}%")
print(f"Time in the {city} is {current_time_in_city} and time in the Czech Republic is {current_time_in_czech}")