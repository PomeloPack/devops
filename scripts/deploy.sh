#!/bin/bash
set -e

echo "=== Checking if Minikube is running ==="
if ! minikube status >/dev/null 2>&1; then
    echo "Minikube is not running. Starting now..."
    minikube start
fi

echo "=== Switching Docker to Minikube environment ==="
eval $(minikube -p minikube docker-env)

echo "=== Building backend Docker image ==="
docker build -t devops-web_be:latest ./backend

echo "=== Building frontend Docker image ==="
docker build -t devops-web_fe:latest ./frontend

echo "=== Running backend tests ==="
if [ -d tests ]; then
    echo "Setting PYTHONPATH to include backend folder..."
    export PYTHONPATH=$(pwd)      # root projektu, aby Python viděl backend balíček
    if pytest tests; then
        echo "Backend tests passed!"
    else
        echo "Backend tests failed!"
        exit 1
    fi
else
    echo "No backend tests directory found, skipping tests."
fi

echo "=== Applying Kubernetes manifests ==="
kubectl apply -f k8s/

echo "=== Loading images into Minikube (recommended) ==="
minikube image load devops-web_be:latest
minikube image load devops-web_fe:latest

echo "=== Checking rollout status ==="
kubectl rollout status deployment/weather-backend
kubectl rollout status deployment/weather-frontend

echo "=== Deployment completed successfully ==="
kubectl get pods -o wide