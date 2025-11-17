from flask import Flask, jsonify, request, g, Response
from dotenv import load_dotenv
from pathlib import Path
import requests
import os
import time
import datetime as dt   
import random
import pytz
import logger_configuration
from sqlalchemy import create_engine
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.exc import OperationalError
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

logger = logger_configuration.logger

# env load
if os.getenv("RUNNING_IN_DOCKER") != "1":
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app)

# PostgreSQL config 
if os.getenv("RUNNING_IN_DOCKER") == "1":
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DOCKER")
else:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

if not SQLALCHEMY_DATABASE_URI:
    raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set!")

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#  Prometheus metrics - not fully finished
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Request latency', ['endpoint'])

@app.before_request
def start_timer():
    g.start = time.time()

@app.after_request
def record_metrics(response):
    resp_time = time.time() - g.start
    REQUEST_LATENCY.labels(request.path).observe(resp_time)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# DB initialization 
def init_db():
    for i in range(10):
        try:
            with app.app_context():
                db.create_all()
            logger.info("DB connected.")
            break
        except OperationalError:
            logger.warning(f"Waiting for DB... attempt {i+1}/10")
            time.sleep(2)
    else:
        logger.error("DB not connected after 10 attempts.")
        exit(1)

local_tz = pytz.timezone('Europe/Prague')
timestmp_local = dt.datetime.now(local_tz)

# Models for db
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

with app.app_context():
    db.create_all()

# API Key - found it .env
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found from env var")
logger.info("API_KEY loaded: %s****", api_key[:4])


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
        response.raise_for_status()
        logger.info("API request successful for city: %s", city)
        return response.json()
    except Exception as e:
        logger.error("Failed API request for city %s: %s", city, e)
        return None

def get_weather_for_city(city):
    response = fetch_weather_data(city)
    if not response:
        return None
    try:
        temp_kelvin = response["main"]["temp"]
        temp_c, temp_f = temp_kelvin_to_celsius(temp_kelvin)
        feels_c, feels_f = temp_kelvin_to_celsius(response["main"]["feels_like"])
        wind_speed = response["wind"]["speed"]
        humidity = response["main"]["humidity"]
        description = response["weather"][0]["description"]

        sunrise = dt.datetime.fromtimestamp(response["sys"]["sunrise"] + response["timezone"], dt.timezone.utc)
        sunset = dt.datetime.fromtimestamp(response["sys"]["sunset"] + response["timezone"], dt.timezone.utc)

        city_tz = pytz.timezone(city_timezones[city])
        czech_tz = pytz.timezone('Europe/Prague')
        local_time_city = dt.datetime.now(city_tz).strftime('%H:%M:%S')
        local_time_czech = dt.datetime.now(czech_tz).strftime('%H:%M:%S')

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
        logger.error("Missing data for city %s: %s", city, e)
        return None
    except Exception as e:
        db.session.rollback()
        logger.error("DB save failed: %s", e)
        return None

# Endpoints how to test it in readme
@app.route("/weather")
def weather_endpoint():
    city = request.args.get("city") or random.choice(city_list)
    data = get_weather_for_city(city)
    if data:
        return jsonify(data)
    return jsonify({"error": "Failed to fetch weather data"}), 500

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/data")
def get_data():
    logs = WeatherAppDb.query.order_by(WeatherAppDb.timestamp.desc()).limit(10).all()
    return jsonify([
        {
            "id": log.id,
            "city": log.city,
            "temp_c": log.temp_c,
            "temp_f": log.temp_f,
            "feels_c": log.feels_c,
            "feels_f": log.feels_f,
            "description": log.description,
            "wind_speed": log.wind_speed,
            "humidity": log.humidity,
            "sunrise": log.sunrise.strftime('%Y-%m-%d %H:%M:%S') if log.sunrise else None,
            "sunset": log.sunset.strftime('%Y-%m-%d %H:%M:%S') if log.sunset else None,
            "local_time_city": log.local_time_city,
            "local_time_czech": log.local_time_czech,
            "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S') if log.timestamp else None
        } for log in logs
    ])

@app.route("/data", methods=["POST"])
def add_data():
    new_entry = request.get_json()
    log = WeatherAppDb(
        city=new_entry.get("city", "Manual"),
        temp_c=new_entry.get("temp_c"),
        temp_f=new_entry.get("temp_f"),
        feels_c=new_entry.get("feels_c"),
        feels_f=new_entry.get("feels_f"),
        description=new_entry.get("description"),
        wind_speed=new_entry.get("wind_speed"),
        humidity=new_entry.get("humidity"),
        sunrise=new_entry.get("sunrise"),
        sunset=new_entry.get("sunset"),
        local_time_city=new_entry.get("local_time_city"),
        local_time_czech=new_entry.get("local_time_czech")
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({"message": "Data stored"}), 201

@app.route("/cities")
def cities_endpoint():
    return jsonify(city_list)

@app.route("/")
def home():
    return "<h1>WeatherApp</h1>"

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5500, debug=True) #5500 run no docker backend - for local testing use different port