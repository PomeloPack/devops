from flask import Flask, jsonify, request
import requests
import datetime as dt
import random
import pytz
import logger_configuration
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

logger = logger_configuration.logger

app = Flask(__name__)
CORS(app)

# postgre config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pomelo:pomeloheslo@localhost:5432/weather_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# utc to cest for saving time into db in czech timezone
local_tz = pytz.timezone('Europe/Prague')
timestmp_local = dt.datetime.now(local_tz)

# table weather log
class WeatherAppDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temp_c = db.Column(db.Float)
    temp_f = db.Column(db.Float)
    feels_c = db.Column(db.Float)
    feels_f = db.Column(db.Float)
    description = db.Column(db.String(100))
    wind_speed = db.Column(db.String(100))
    humidity = db.Column(db.String(100))
    sunrise = db.Column(db.DateTime(timezone=True))
    sunset = db.Column(db.DateTime(timezone=True))
    local_time_city = db.Column(db.String(50))
    local_time_czech = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())

# create a table if not exist
with app.app_context():
    db.create_all()

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

def temp_kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * 9/5 + 32
    return round(celsius, 2), round(fahrenheit, 2)

def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # vyhodí HTTPError, pokud status != 200
        logger.info("API request successful for city: %s", city)
        return response.json()
    except Exception as e:
        logger.error("Failed to make API request for city %s: %s", city, e)
        return None

def get_weather_for_city(city):
    """Funkce, která připraví JSON pro frontend"""
    response = fetch_weather_data(city)
    if not response:
        return None

    try:
        temp_kelvin = response["main"]["temp"]
        temp_c, temp_f = temp_kelvin_to_celsius(temp_kelvin)
        feels_kelvin = response["main"]["feels_like"]
        feels_c, feels_f = temp_kelvin_to_celsius(feels_kelvin)
        wind_speed = response["wind"]["speed"]
        humidity = response["main"]["humidity"]
        description = response["weather"][0]["description"]

        sunrise = dt.datetime.fromtimestamp(response["sys"]["sunrise"] + response["timezone"], dt.timezone.utc)
        sunset = dt.datetime.fromtimestamp(response["sys"]["sunset"] + response["timezone"], dt.timezone.utc)

        city_tz = pytz.timezone(city_timezones[city])
        czech_tz = pytz.timezone('Europe/Prague')
        local_time_city = dt.datetime.now(city_tz).strftime('%H:%M:%S')
        local_time_czech = dt.datetime.now(czech_tz).strftime('%H:%M:%S')

        # save to db
        log = WeatherAppDb(
            city=city,
            temp_c=temp_c,
            temp_f=temp_f,
            feels_c=feels_c,
            feels_f=feels_f,
            description=description,
            wind_speed=str(wind_speed),
            humidity=str(humidity),
            sunrise=sunrise,
            sunset=sunset,
            local_time_city=local_time_city,
            local_time_czech=local_time_czech,
        )
        db.session.add(log)
        db.session.commit()

        return {
            "city": city,
            "temp_c": temp_c,
            "temp_f": temp_f,
            "feels_c": feels_c,
            "feels_f": feels_f,
            "wind_speed": wind_speed,
            "humidity": humidity,
            "description": description,
            "sunrise": sunrise.strftime('%H:%M:%S'),
            "sunset": sunset.strftime('%H:%M:%S'),
            "local_time_city": local_time_city,
            "local_time_czech": local_time_czech
        }
    
    except KeyError as e:
        logger.error("Failed to retrieve data from response for city %s: %s", city, e)
        return None
    except Exception as e:
        db.session.rollback()
        logger.error('Failed to save to DB: %s', e)
        return None

# Upravený endpoint, který přijímá parametr city
@app.route("/weather")
def weather_endpoint():
    city = request.args.get("city")  # získat city z query param
    if not city:
        city = random.choice(city_list)  # fallback, pokud není parametr zadán

    data = get_weather_for_city(city)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5500, debug=True)  # port 5500 pro tvůj server