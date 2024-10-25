import requests
import datetime as dt
import json
import random


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

def temp_kelvin_to_celsium(kelvin):
    celsium = kelvin - 273.15
    fahrenheit = celsium * 9/5 + 32
    return celsium, fahrenheit

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

response = requests.get(url).json()



temp_kelvin = (response["main"]["temp"])
temp_celsium, temp_fahrenheit = temp_kelvin_to_celsium(temp_kelvin)
maybe_like_kelvin = response["main"]["feels_like"]
maybe_like_celsium, maybe_like_fahrenheit = temp_kelvin_to_celsium(maybe_like_kelvin)
wind_speed = response["wind"]["speed"]
humidity = response["main"]["humidity"]
description = response["weather"][0]["description"]
sunrise_time = dt.datetime.utcfromtimestamp(response["sys"]["sunrise"] + response["timezone"])
sunset_time = dt.datetime.utcfromtimestamp(response["sys"]["sunset"] + response["timezone"])

print(f"Name of the city: {city}")
print(f"Description in {city}: {description}")
print(f"Temperature in {city}: {temp_celsium:.2f}°C or {temp_fahrenheit:.2f}°F")
print(f"Temperature in {city} feels like: {maybe_like_celsium:.2f}°C or {maybe_like_fahrenheit:.2f}°F")
print(f"General weather in {city}: {description}")
print(f"Sunrise in {city}: {sunrise_time} local time")
print(f"Sunset in {city}: {sunset_time} local time")
print(f"Wind speed in {city}: {wind_speed} m/s")
print(f"Humidity in {city}: {humidity}%")