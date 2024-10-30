FROM python
WORKDIR /home/p0m3l0/Project/devops/weather_app_for_docker.py
COPY . /home/p0m3l0/Project/devops/weather_app_for_docker.py
CMD ["python", "weather_app_for_docker.py"]