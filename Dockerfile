FROM python
WORKDIR /devops/weather_app-image/weather_app_for_docker.py
COPY . /devops/weather_app-image/weather_app_for_docker.py
CMD ["python", "weather_app_for_docker.py"]