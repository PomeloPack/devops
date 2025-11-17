FROM python:3.12-slim
# non root usera
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
# create a repository for logs and settings
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
CMD ["python", "weather_app.py"]