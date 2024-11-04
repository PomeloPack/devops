#FROM python
#WORKDIR /home/p0m3l0/Project/devops
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#COPY . .
#CMD ["python", "weather_app_for_docker.py"]

FROM python:3.12

ADD weather_app_for_docker.py .

RUN pip install -r requirements.txt

CMD ["python", "./weather_app_for_docker.py"]