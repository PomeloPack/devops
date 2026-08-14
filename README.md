# Weather App — DevOps Playground

[![CI Pipeline](https://github.com/PomeloPack/devops/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/PomeloPack/devops/actions/workflows/ci-cd.yml)

A small weather-tracking application used as an end-to-end DevOps sandbox: containerized services, metrics, dashboards, Kubernetes manifests, and a CI pipeline, all built around a simple Flask + PostgreSQL app.

The app itself calls the OpenWeather API and stores results (temperature, humidity, sunrise/sunset, local time, etc.) for a fixed list of cities.

## Stack

| Layer         | Technology                                   |
|---------------|-----------------------------------------------|
| Frontend      | Static HTML/JS, served by Nginx                |
| Backend       | Python / Flask + SQLAlchemy                    |
| Database      | PostgreSQL 16                                  |
| Metrics       | Prometheus (`/metrics` endpoint)               |
| Dashboards    | Grafana                                        |
| Orchestration | Docker Compose (local), Kubernetes (Minikube)  |
| CI            | GitHub Actions                                 |

## Architecture

```
┌─────────────────────┐      HTTP (/weather)      ┌──────────────────────┐
│       Frontend       │ ────────────────────────▶ │       Backend         │
│  HTML / JS / Fetch   │                            │  Flask + SQLAlchemy   │
└─────────────────────┘                            │  OpenWeather client   │
                                                    └──────────┬───────────┘
                                                               │ SQL
                                                               ▼
                                                    ┌──────────────────────┐
                                                    │      PostgreSQL       │
                                                    └──────────────────────┘

Prometheus scrapes /metrics on the backend → Grafana visualizes it.
```

## Project Structure

```
.
├── backend/            Flask API, Dockerfile, requirements
├── frontend/            Static HTML/JS, Nginx Dockerfile
├── k8s/                 Kubernetes manifests (Minikube-oriented)
├── prometheus/          Prometheus config
├── grafana/             Grafana dashboard JSON
├── scripts/             deploy.sh, stress_test.sh, traffic_generator.sh
├── tests/                pytest suite (API, DB, models, routes)
├── .github/workflows/    CI pipeline
└── docker-compose.yml
```

## Prerequisites

- Docker & Docker Compose
- Python 3.13 (only needed for running the backend outside Docker)
- Minikube (for the Kubernetes path)
- An OpenWeather API key

## Configuration

Copy the example env file and fill in real values:

```bash
cp .env.example .env
```

```
BACKEND_URL=http://localhost:8000
DB_USER=youruser
DB_PASSWORD=yourpassword
API_KEY=your_openweather_api_key
```

`.env` and the Postgres data directory (`db_data/`) are gitignored — never commit either.

## Running with Docker Compose

```bash
docker compose up --build
```

| Service     | URL                              |
|-------------|-----------------------------------|
| Frontend    | http://localhost:8080             |
| Backend     | http://localhost:5500/weather     |
| Database    | localhost:5433                    |
| Prometheus  | http://localhost:9090             |
| Grafana     | http://localhost:3000 (default login `admin` / `admin`, change on first login) |

If a fetch fails with a missing API key, make sure it's exported into the shell environment before compose picks it up:

```bash
export $(cat .env | xargs)
```

To reset a broken local stack:

```bash
docker compose down
docker system prune -af
docker compose up --build
```

Check container logs if something looks wrong:

```bash
docker logs weather_backend
docker logs weather_frontend
```

## API Reference

**Health check**

```bash
curl http://localhost:5500/health
# {"status": "ok"}
```

**Latest readings** (last 10 rows)

```bash
curl http://localhost:5500/data
```

```json
{
  "city": "Mexico City",
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
  "wind_speed": "3.09"
}
```

**Insert a reading manually**

```bash
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
# {"message": "Data stored"}
```

**List supported cities**

```bash
curl http://localhost:5500/cities
```

**Prometheus metrics**

```bash
curl http://localhost:5500/metrics
```

## Database

```bash
# Local Postgres (Compose maps 5432 -> 5433 on the host)
psql -h localhost -p 5433 -U pomelo -d weather_app

# Or straight into the running container
docker exec -it weather_db psql -U pomelo -d weather_app
```

```
Table "public.weather_app_db"
      Column      |           Type           | Nullable |                  Default
------------------+--------------------------+----------+---------------------------------------------
 id               | integer                  | not null | nextval('weather_app_db_id_seq'::regclass)
 city             | character varying(100)   | not null |
 temp_c           | double precision         |          |
 temp_f           | double precision         |          |
 feels_c          | double precision         |          |
 feels_f          | double precision         |          |
 description      | character varying(100)   |          |
 wind_speed       | character varying(100)   |          |
 humidity         | character varying(100)   |          |
 sunrise          | timestamp with time zone |          |
 sunset           | timestamp with time zone |          |
 local_time_city  | character varying(50)    |          |
 local_time_czech | character varying(50)    |          |
 timestamp        | timestamp with time zone |          | now()
```

## Running Without Docker

**Frontend** — open `frontend/index.html` with a Live Server extension and use the dashboard directly.

**Backend** — install dependencies and run:

```bash
pip install -r backend/requirements.txt
python backend/weather_app.py
```

The whole stack (DB included) is designed to run in Docker — running the backend bare is mainly useful for quick debugging.

## Kubernetes (Minikube)

```bash
minikube start --driver=docker
eval $(minikube -p minikube docker-env)

# Build images directly into Minikube's Docker daemon
docker build -t devops-web_be ./backend
docker build -t devops-web_fe ./frontend

# API key as a Secret (replace with your real key)
kubectl create secret generic weather-api-key --from-literal=API_KEY=<your-api-key>

kubectl apply -f k8s/config-map.yaml
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/frontend-configmap.yaml
```

```bash
kubectl get pods
kubectl logs <pod-name>
kubectl port-forward svc/weather-backend 5000:5000
kubectl port-forward svc/weather-frontend 8080:80
```

Or run the whole thing with the automation script, which checks Minikube, builds both images, loads them into the cluster, runs backend tests, applies manifests, and verifies the rollout:

```bash
./scripts/deploy.sh
```

## Testing

```bash
pip install -r tests/requirements_for_test.txt
export PYTHONPATH=$(pwd):$(pwd)/backend
pytest -v tests/
```

Covers API endpoints, city list/timezone data, DB models, and route handlers. The same suite runs in CI on every push/PR to `main`.

## CI/CD

GitHub Actions (`.github/workflows/ci-cd.yml`) on every push/PR to `main`:

1. Build the frontend (if `package.json` exists)
2. Install backend dependencies and run the pytest suite (against SQLite)
3. Build backend and frontend Docker images

Kubernetes deployment is intentionally left as a manual step (`./scripts/deploy.sh` against Minikube) rather than wired into CI.

## Known Issues

- Routing between frontend and backend behaves differently across local / Docker / Minikube due to CORS and port mapping differences. Works with manual port-forwarding, but isn't fully automated yet.

## Roadmap

- [ ] Loki + Promtail for centralized log aggregation alongside metrics
- [ ] Redis caching layer
- [ ] Broader test coverage for DB interactions and deployment validation
- [ ] CI/CD: rollback strategy, multi-environment support, image security scanning
- [ ] Kubernetes: Helm charts, tighter secrets management for all credentials (not just the API key)
- [ ] ArgoCD for GitOps-driven deployment
- [ ] Terraform-provisioned cloud infrastructure (AWS/Oracle Cloud free tier)

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
