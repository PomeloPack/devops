README.md — Weather Application 

This project is a complete DevOps-ready application composed of:

- **Python/Flask backend**
- **HTML/JavaScript frontend**  
- **PostgreSQL database**  
- **Prometheus metrics**  
- **Grafana dashboards**  
- **Docker & Docker Compose orchestration**  
- **Kubernetes manifests**  
- **CI/CD pipeline configuration (GitHub Actions or GitLab CI)**  

The goal of the project is to demonstrate ability to design, containerize, deploy, monitor, and document a simple cloud-native application.

---
Architecture Overview

The system consists of three main components:

- **Frontend** – Static HTML/JS, calling the backend via REST  
- **Backend** – Flask API + PostgreSQL + OpenWeather integration  
- **Database** – Stores cities & fetched weather results  

Monitoring is enabled via Prometheus scraping backend metrics.

                    ┌────────────────────────────────────┐
                    │              FRONTEND               │
                    │     HTML / JavaScript / Fetch API   │
                    └───────────────────┬──────────────────┘
                                        │ HTTP Request (/weather)
                                        ▼
                    ┌────────────────────────────────────┐
                    │               BACKEND               │
                    │     Flask API + SQLAlchemy ORM      │
                    │     Integrates with OpenWeather     │
                    └───────────────────┬──────────────────┘
                                        │ SQL Queries
                                        ▼
                    ┌────────────────────────────────────┐
                    │                 DB                  │
                    │          PostgreSQL Database        │
                    └────────────────────────────────────┘

---

Main Project Structure:

├── README.md
├── docker-compose.yml
├── .gitignore

├── backend/
│   ├── weather_app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── …

├── frontend/
│   ├── index.html
│   ├── Dockerfile
│   └── …

├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── …

├── prometheus/
│   └── prometheus.yaml

├── grafana/
│   └── dashboards/
│       └── weather-dashboard.json

├── scripts/
│   └── deploy.sh

├── .github/workflows/
│   └── ci.yml

└── tests/
├── test_api.py
├── test_cities.py
├── test_models.py
└── test_routes.py

---

Prerequisites:

- Docker
- Docker Compose
- Minikube ( k8s Testing)
- Install requirements.txt ( pip install -r requirements.txt)
- Live Server for FE
- Python3.12

---

Running Locally (Without Docker) - Backend

from root folder come to **backend**
pip install -r requirements.txt
**export** SQLALCHEMY_DATABASE_URI=“postgresql://pomelo:pomeloheslo@localhost:5433/weather_app” ( in the app use .env) - DB run only on docker - must be always UP
**USE** : 
docker run --name weather_db \
    -e POSTGRES_USER=pomelo \
    -e POSTGRES_PASSWORD=pomeloheslo \
    -e POSTGRES_DB=weather_app \
    -p 5433:5432 \
    -v postgres_data:/var/lib/postgresql/data \
    postgres:16
and **docker ps**
result will be:
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                                         NAMES
78dca2435191   postgres:16   "docker-entrypoint.s…"   24 minutes ago   Up 24 minutes   0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp   weather_db
run the BE: python3 weather_app.py
You can test backend API from the terminal use:

cURL health:
http://localhost:5500/health - for heatl status

Response:
curl http://localhost:5500/health
{
  "status": "ok"
}

cURL GET:
http://localhost:5500/data

Response:
{"city": "Mexico City",
    "description": "clear sky",
    "feels_c": 21.47,
    "feels_f": 70.65,
    "humidity": "15",
    "id": 3,
    "local_time_city": "13:13:53",
    "local_time_czech": "20:13:53",
    "sunrise": "2025-11-16 06:45:23",
    "sunset": "2025-11-16 17:57:34",
    "temp_c": 22.75,
    "temp_f": 72.95,
    "timestamp": "2025-11-16 19:13:53",
    "wind_speed": "3.09"}

You will see max last 10 records from the database

cURL POST:
  curl -X POST http://localhost:5500/data \
-H "Content-Type: application/json" \
-d '{
    "city": "Prague",
    "temp_c": 20.5,
    "temp_f": 68.9,
    "feels_c": 19.0,
    "feels_f": 66.2,
    "description": "sunny",
    "wind_speed": "5 km/h",
    "humidity": "60%",
    "sunrise": "2025-11-12T07:00:00",
    "sunset": "2025-11-12T16:30:00",
    "local_time_city": "14:30:00",
    "local_time_czech": "14:30:00"
}'

Response:
{
  "message": "Data stored"
}


---

Postgre DB settings:

in the terminal use: 
for local - psql -h localhost -p 5433 -U pomelo -d weather_app
for docker - docker exec -it weather_db psql -U pomelo -d weather_app

            List of relations
 Schema |      Name      | Type  | Owner  
--------+----------------+-------+--------
 public | weather_app_db | table | pomelo

                                          Table "public.weather_app_db"
      Column      |           Type           | Collation | Nullable |                  Default                   
------------------+--------------------------+-----------+----------+--------------------------------------------
 id               | integer                  |           | not null | nextval('weather_app_db_id_seq'::regclass)
 city             | character varying(100)   |           | not null | 
 temp_c           | double precision         |           |          | 
 temp_f           | double precision         |           |          | 
 feels_c          | double precision         |           |          | 
 feels_f          | double precision         |           |          | 
 description      | character varying(100)   |           |          | 
 wind_speed       | character varying(100)   |           |          | 
 humidity         | character varying(100)   |           |          | 
 sunrise          | timestamp with time zone |           |          | 
 sunset           | timestamp with time zone |           |          | 
 local_time_city  | character varying(50)    |           |          | 
 local_time_czech | character varying(50)    |           |          | 
 timestamp        | timestamp with time zone |           |          | now()
Indexes:
    "weather_app_db_pkey" PRIMARY KEY, btree (id)

---

Run Locally (Without Docker) - FrontEnd

Right click to **index.html**
Open with Live Server
You will be redirected to browser where you will see the Weather Dashborad.
Click to Get Weather and you will see the stats which will be saved into the postgre database.

---

Running with Docker Compose:

**docker compose up --build**
you will see this:

[+] Running 29/37
 ⠧ db [⣿⣿⣿⣿⣿⣀⣿⣿⣿⣿⣿⣿⣿⣿] 81.52MB / 158.7MB Pulling                                                                                                                                             46.7s 
 ⠧ grafana [⣿⣿⣿⣿⣤⣿⣦⣿⣿⣿] 111.2MB / 187MB   Pulling                                                                                                                                            46.7s 
 ⠧ prometheus [⣿⣿⣿⣶⣷⣿⣿⣿⣿⣿] 107.4MB / 124.5MB Pulling 

 Waint until all parts of container will be successfully instaled.

Access:

- **Frontend:** http://localhost:8080  
- **Backend:** http://localhost:5500/weather  
- **Database:** localhost:5433 

**docker images** to check the images of the docker:
docker images
REPOSITORY        TAG       IMAGE ID       CREATED        SIZE
devops-web_be     latest    2d860387d50e   15 hours ago   276MB
devops-web_fe     latest    a073908c8c14   15 hours ago   80.9MB
postgres          16        74bbe2dbc3c3   2 days ago     657MB
prom/prometheus   latest    49214755b615   2 weeks ago    472MB
grafana/grafana   latest    35c41e0fd029   3 weeks ago    909MB

**docker ps** for running containers:
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS                                         NAMES
9c0023f214c9   grafana/grafana:latest   "/run.sh"                7 seconds ago   Up 6 seconds   0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp   grafana
973c8136671c   devops-web_fe            "/docker-entrypoint.…"   7 seconds ago   Up 6 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp       weather_frontend
75c3131a218e   prom/prometheus:latest   "/bin/prometheus --c…"   7 seconds ago   Up 6 seconds   0.0.0.0:9090->9090/tcp, [::]:9090->9090/tcp   prometheus
b8be136852b1   devops-web_be            "python weather_app.…"   7 seconds ago   Up 6 seconds   0.0.0.0:5500->5500/tcp, [::]:5500->5500/tcp   weather_backend
32f3c7b67419   postgres:16              "docker-entrypoint.s…"   7 seconds ago   Up 6 seconds   0.0.0.0:5433->5432/tcp, [::]:5433->5432/tcp   weather_db

Now you will be able to test whole appliation with the docker.

for example healt ( same what we test locally now just running via docker)

cURL:
http://localhost:5500/health

response:
{
  "status": "ok"
}

If something doesn't work please check the logs:

docker logs weather_backend
docker logs weather_frontend

or on the front end use dev tools ( browser - network)

hint:
if yout build docker compose before and anything works wrong - restrat it

**docker compose down**
**docker system prine -af**
**docker compose up --buidl**

In the docker sometimes you must use this:
export $(cat .env | xargs)
to export API key from .env to fetch data

---

Kubernetes - minuikube running:

Start minikube:

minikube start --driver=docker
😄  minikube v1.37.0 on Darwin 26.1 (arm64)
✨  Using the docker driver based on existing profile
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.48 ...
🤷  docker "minikube" container is missing, will recreate.
🔥  Creating docker container (CPUs=2, Memory=4000MB) ...
🐳  Preparing Kubernetes v1.34.0 on Docker 28.4.0 ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
hint: if there is any problem with start minikube use command **minikube delete** and start it again

minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

Docker CLI for MINIKUBE - build into cluster

eval $(minikube -p minikube docker-env)

Checking of nodes and pods

kubectl get nodes

NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   2m5s   v1.34.0

kubectl get pods -A

NAMESPACE     NAME                               READY   STATUS    RESTARTS   AGE
kube-system   coredns-66bc5c9577-wr2j2           1/1     Running   0          2m16s
kube-system   etcd-minikube                      1/1     Running   0          2m22s
kube-system   kube-apiserver-minikube            1/1     Running   0          2m23s
kube-system   kube-controller-manager-minikube   1/1     Running   0          2m22s
kube-system   kube-proxy-9bjrm                   1/1     Running   0          2m16s
kube-system   kube-scheduler-minikube            1/1     Running   0          2m22s
kube-system   storage-provisioner                1/1     Running   0          2m21s

Build docker image for BE + FE

docker build -t devops-web_be ./backend
docker build -t devops-web_fe ./frontend

Deploy into minikube

kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/config-map.yaml
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml

after deleting minikube and all the data use:

kubectl create secret generic weather-api-key \
  --from-literal=API_KEY=0060cf5abb2bfda0140d4fc62051bb9e
secret/weather-api-key created

use command **kubectl get pods**

NAME                                READY   STATUS    RESTARTS   AGE
weather-backend-74658dcb5d-jsjfw    1/1     Running   0          20s
weather-backend-74658dcb5d-m7j65    1/1     Running   0          20s
weather-db-786868f9d6-ldkt4         1/1     Running   0          3m31s
weather-frontend-57f66ccd59-2rpg9   1/1     Running   0          3m31s

View logs for troubleshooting:

kubectl logs <pod-name>

Acess BE from FE pod:

kubectl exec -it weather-frontend-8d45b7f4f-hlvxz -- curl -s http://weather-backend:5500/health

{
  "status": "ok"
}

Automation deploy shell script:

./scripts/deploy.sh

This script will do:

CHeck if minikube is running
Switch Docker to Minikibe env
build BE docker IMAGE
build FE docker IMAGE
Load images into Minikube
Running BE test

---

ArgoCD:

Is implemented,
in the terminal use: kubectl port-forward svc/argocd-server -n argocd 8080:443
WEB URL: https://localhost:8080/login?return_url=https%3A%2F%2Flocalhost%3A8080%2Fapplications

user: admin
passwd: zqvD2FRSkvXeqmso





---

Next Steps / Future Work

While the core functionality is fully implemented, the following enhancements would be completed with more time:
	1.	Monitoring and Observability
	•	Expose application metrics (/metrics) for Prometheus.
	•	Create Grafana dashboards to visualize request rates, latency, errors, and business metrics.
	•	Optionally add tracing for end-to-end request tracking.
	2.	Caching (Redis)
	•	Add Redis service for caching in Docker Compose and Kubernetes.
	•	Integrate caching in the application to improve performance.
	3.	Testing
	•	Expand unit and integration test coverage for all endpoints.
	•	Add automated tests for database interactions and deployment validation.
	4.	CI/CD Enhancements
	•	Implement rollback strategies and deployment validation in GitHub Actions.
	•	Add support for multiple environments (dev/staging/prod).
	•	Integrate security scanning for Docker images.
	5.	Kubernetes Improvements
	•	Add resource limits and requests to all containers.
	•	Use Helm charts for parameterized deployments.
	•	Introduce secrets management for sensitive configuration.