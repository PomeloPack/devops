FROM python:3.12-slim
WORKDIR /home/p0m3l0/Project/devops
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "weather_app.py"]