from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
api_key = "0060cf5abb2bfda0140d4fc62051bb9e"

@app.route("/weather")
def get_weather():
    city = request.args.get("city")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        resp = requests.get(url)
        data = resp.json()
        temp_c, temp_f = temp_kelvin_to_celsium(data['main']['temp'])
        return jsonify({
            "city": city,
            "temp_c": temp_c,
            "temp_f": temp_f,
            "weather": data['weather'][0]['description']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500