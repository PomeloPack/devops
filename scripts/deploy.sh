#!/bin/bash
set -e

# check if minikube is running
echo "=== Checking if Minikube is running ==="
if ! minikube status >/dev/null 2>&1; then
    echo "Minikube is not running. Starting now..."
    minikube start
fi

# switch Docker CLI to Minikube 
echo "=== Switching Docker to Minikube environment ==="
eval $(minikube -p minikube docker-env)

# Build Docker image backend/frontend
echo "=== Building backend Docker image ==="
docker build -t devops-web_be:latest ./backend

echo "=== Building frontend Docker image ==="
docker build -t devops-web_fe:latest ./frontend

# loadimage into Minikube
echo "=== Loading images into Minikube ==="
minikube image load devops-web_be:latest
minikube image load devops-web_fe:latest

# be tests
echo "=== Running backend tests ==="
if [ -d tests ]; then
    echo "Setting PYTHONPATH to include backend folder..."
    export PYTHONPATH=$(pwd)/backend 
    if pytest tests; then
        echo "Backend tests passed!"
    else
        echo "Backend tests failed!"
        exit 1
    fi
else
    echo "No backend tests directory found, skipping tests."
fi

#  k8s manifests
echo "=== Applying Kubernetes manifests ==="
kubectl apply -f k8s/config-map.yaml
kubectl apply -f k8s/db-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/frontend-configmap.yaml

# rollout check
echo "=== Checking rollout status ==="
kubectl rollout status deployment/weather-db
kubectl rollout status deployment/weather-backend
kubectl rollout status deployment/weather-frontend

# BE check
echo "=== Checking backend health endpoint ==="
BACKEND_URL=$(minikube service weather-backend --url)
echo "Backend URL: $BACKEND_URL"
curl -f "$BACKEND_URL/health" && echo "Backend is healthy!" || echo "Backend health check failed!"

echo "=== Deployment completed successfully ==="
kubectl get pods -o wide

# access FE thru minikube nodeport
FRONTEND_URL=$(minikube service weather-frontend --url)
echo "Frontend URL: $FRONTEND_URL"
echo "Open this URL in your browser to access the Weather Dashboard."