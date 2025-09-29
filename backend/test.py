import requests
api_key = "0060cf5abb2bfda0140d4fc62051bb9e"
city = "Prague"
r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
print(r.json())