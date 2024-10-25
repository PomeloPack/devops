import requests
import datetime as dt
import tkinter as tk
from tkinter import messagebox
import json
import random

# List of cities
city_list = [
    "London", "New York", "Paris", "Tokyo", "Sydney",
    "Rio de Janeiro", "Moscow", "Berlin", "Rome", "Dubai",
    "Beijing", "Mumbai", "Cairo", "Istanbul", "Toronto",
    "Seoul", "Bangkok", "Singapore", "Delhi", "Amsterdam",
    "Vienna", "Hamburg", "Osaka", "Milan", "Madrid",
    "Barcelona", "Lima", "Buenos Aires", "Lagos", "Mexico City",
    "Sao Paulo", "Jakarta", "Kuala Lumpur", "Shanghai", "Istanbul",
    "Moscow", "Rio de Janeiro", "Tokyo", "Paris", "Prague", "Brno"
]

# Create main screen for app
root = tk.Tk()
root.title("Weather App for DevOps Testing")

# Full configuration below:
# Labels and fields
city_label = tk.Label(root, text="City (leave blank for random)")
city_label.pack()
city_entry = tk.Entry(root)
city_entry.pack()

# Button for fetching data
fetch_button = tk.Button(root, text="Fetch Weather")
fetch_button.pack()

# Create a label to display weather information
weather_label = tk.Label(root)
weather_label.pack()

# Define the function to fetch weather data
def fetch_weather():
    # Randomly select a city if entry is blank
    city = city_entry.get()
    if city.strip() == "":
        city = random.choice(city_list)
    
    # Add your API key here
    api_key = "0060cf5abb2bfda0140d4fc62051bb9e"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature_kelvin = data["main"]["temp"]
            temperature_celsius = temperature_kelvin - 273.15
            weather = data["weather"][0]["description"]
            weather_label.config(text=f"City: {city}\nTemperature: {temperature_celsius:.2f}°C\nWeather: {weather.capitalize()}")
        elif response.status_code == 401:
            messagebox.showerror("Error", "Unauthorized: Check your API key.")
        else:
            messagebox.showerror("Error", f"City not found. Status code: {response.status_code}")   
    
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data")

fetch_button.config(command=fetch_weather)

# Start the GUI main loop
root.mainloop()
