#!/bin/bash
set -e

echo "=== Setting up Minikube Docker environment ==="
eval $(minikube -p minikube docker-env)

echo "=== Building backend image ==="
docker build -t devops-web_be:latest ./backend

echo "=== Building frontend image ==="
docker build -t devops-web_fe:latest ./frontend

echo "=== Running backend tests ==="
cd backend
pytest || (echo " Tests failed" && exit 1)
cd ..

echo "=== Applying Kubernetes manifests ==="
kubectl apply -f k8s/

echo "=== Checking rollout status ==="
kubectl rollout status deployment/weather-backend
kubectl rollout status deployment/weather-frontend

echo "=== All done ==="
kubectl get pods