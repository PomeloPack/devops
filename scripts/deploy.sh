#!/bin/bash
set -e

echo "=== Checking if Minikube is running ==="
if ! minikube status >/dev/null 2>&1; then
    echo "Minikube is not running. Starting now..."
    minikube start
fi

echo "=== Switching Docker to Minikube env ==="
eval $(minikube -p minikube docker-env)

echo "=== Building backend image ==="
docker build -t devops-web_be:latest ./backend

echo "=== Building frontend image ==="
docker build -t devops-web_fe:latest ./frontend

echo "=== Running backend tests ==="
if [ -d backend ]; then
    cd backend
    if pytest; then
        echo "Tests passed!"
    else
        echo "Tests failed!"
        exit 1
    fi
    cd ..
else
    echo "Backend directory not found!"
    exit 1
fi

echo "=== Applying Kubernetes manifests ==="
kubectl apply -f k8s/

echo "=== Loading images into Minikube (optional but recommended) ==="
minikube image load devops-web_be:latest
minikube image load devops-web_fe:latest

echo "=== Checking rollout status ==="
kubectl rollout status deployment/weather-backend
kubectl rollout status deployment/weather-frontend

echo "=== Deploy completed ==="
kubectl get pods -o wide