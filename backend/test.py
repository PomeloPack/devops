from flask import Flask, request, jsonify
import random

app = Flask(__name__)

city_list = ["Prague", "Berlin", "London", "Paris", "Rome"]

def get_weather_for_city(city):
    # Fiktivní data pro testování
    return {
        "city": city,
        "temp_c": round(random.uniform(10, 30), 1),
        "temp_f": round(random.uniform(50, 86), 1),
        "description": random.choice(["Sunny", "Cloudy", "Rainy", "Windy"]),
        "feels_c": round(random.uniform(10, 30), 1),
        "feels_f": round(random.uniform(50, 86), 1),
        "wind": round(random.uniform(0, 10), 1),
        "humidity": random.randint(30, 90)
    }

@app.route("/weather")
def weather_endpoint():
    city = request.args.get("city")  # zkusíme query param
    if not city:
        city = random.choice(city_list)  # fallback: náhodné město

    data = get_weather_for_city(city)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)