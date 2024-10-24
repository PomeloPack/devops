import requests
import datetime as dt
import tkinter as tk
from tkinter import messagebox
import json

#create main screen for app
root = tk.Tk()
root.title("Weather App for DevOps testing")

# full configuation below:
# labels and fields
city_label = tk.Label(root, text="City")
city_label.pack()
city_entry = tk.Entry(root)
city_entry.pack()

# button for fetching data

fetch_button = tk.Button(root, text="Fetch Weather")
fetch_button.pack()

# Create a label to display weather information
weather_label = tk.Label(root)
weather_label.pack()

# Define the function to fetch weather data
def fetch_weather():
    city = city_entry.get()
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
            weather_label.config(text=f"Temperature: {temperature_celsius:.2f}°C\nWeather: {weather.capitalize()}")
        elif response.status_code == 401:
            messagebox.showerror("Error", "Unauthorized: Check your API key.")
        else:
            messagebox.showerror("Error", f"City not found. Status code: {response.status_code}")   
    
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data")

fetch_button.config(command=fetch_weather)

# Start the GUI main loop
root.mainloop()
