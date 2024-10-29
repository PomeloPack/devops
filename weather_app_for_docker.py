import requests
import datetime as dt
import json
import random
import pytz


base_url = "https://api.openweathermap.org/data/2.5/weather?"
api_key = "0060cf5abb2bfda0140d4fc62051bb9e"
city_list = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "San Jose",
    "Austin",
    "Jacksonville",
    "San Francisco",
    "Columbus",
    "Fort Worth",
    "Charlotte",
    "Indianapolis",
    "Seattle",
    "Denver",
    "Washington D.C.",
    "Boston",
    "El Paso",
    "Nashville",
    "Detroit",
    "Oklahoma City",
    "Portland",
    "Las Vegas",
    "Milwaukee",
    "Albuquerque",
    "Tucson",
    "Fresno",
    "Sacramento",
    "Long Beach"
]

city = random.choice(city_list)

city_timezones = {
    "New York": "America/New_York",
    "Los Angeles": "America/Los_Angeles",
    "Chicago": "America/Chicago",
    "Houston": "America/Chicago",
    "Phoenix": "America/Phoenix",
    "Philadelphia": "America/New_York",
    "San Antonio": "America/Chicago",
    "San Diego": "America/Los_Angeles",
    "Dallas": "America/Chicago",
    "San Jose": "America/Los_Angeles",
    "Austin": "America/Chicago",
    "Jacksonville": "America/New_York",
    "San Francisco": "America/Los_Angeles",
    "Columbus": "America/New_York",
    "Fort Worth": "America/Chicago",
    "Charlotte": "America/New_York",
    "Indianapolis": "America/Indianapolis",
    "Seattle": "America/Los_Angeles",
    "Denver": "America/Denver",
    "Washington D.C.": "America/New_York",
    "Boston": "America/New_York",
    "El Paso": "America/Denver",
    "Nashville": "America/Chicago",
    "Detroit": "America/New_York",
    "Oklahoma City": "America/Chicago",
    "Portland": "America/Los_Angeles",
    "Las Vegas": "America/Los_Angeles",
    "Milwaukee": "America/Chicago",
    "Albuquerque": "America/Denver",
    "Tucson": "America/Phoenix",
    "Fresno": "America/Los_Angeles",
    "Sacramento": "America/Los_Angeles",
    "Long Beach": "America/Los_Angeles"
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
print(f"Temperature in {city}: {temp_celsium:.2f}°C or {temp_fahrenheit:.2f}°F")
print(f"Temperature in {city} feels like: {feeling_like_celsium:.2f}°C or {feeling_like_fahrenheit:.2f}°F")
print(f"General weather in {city}: {description}")
print(f"Sunrise in {city}: {sunrise_time} local time")
print(f"Sunset in {city}: {sunset_time} local time")
print(f"Wind speed in {city}: {wind_speed} m/s")
print(f"Humidity in {city}: {humidity}%")
print(f"Time in the {city} is {current_time_in_city} and time in the Czech Republic is {current_time_in_czech}")