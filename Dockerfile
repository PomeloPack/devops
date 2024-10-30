FROM python
WORKDIR /home/p0m3l0/Project/devops
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "weather_app_for_docker.py"]