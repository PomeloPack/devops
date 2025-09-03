import requests

city = "London"
api_key = "0060cf5abb2bfda0140d4fc62051bb9e"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

resp = requests.get(url)
print(resp.status_code)
print(resp.json())