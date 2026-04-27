# Kubernetes Deployment Guide

This guide explains how to deploy the AI Text Analyzer application to a Kubernetes cluster.

## Prerequisites

Before you begin, ensure you have the following:

1.  **Kubernetes Cluster**: A running cluster (e.g., Minikube, Kind, GKE, EKS, or Azure AKS).
2.  **kubectl**: The Kubernetes command-line tool installed and configured to point to your cluster.
3.  **Docker Registry**: An account on Docker Hub (or another registry) to store your image.
4.  **Ingress Controller**: If you plan to use `ingress.yaml`, ensure an ingress controller (like NGINX) is installed in your cluster.

## Steps to Deploy

### 1. Build and Push the Docker Image

First, build your Docker image and push it to Docker Hub so Kubernetes can pull it.

```powershell
# Replace 'c3gowda' with your Docker Hub username if different
docker build -t c3gowda/sentiment-analysis:latest .
docker push c3gowda/sentiment-analysis:latest
```

### 2. Apply Manifests

Run the following commands to create the Deployment, Service, and Ingress resources.

```powershell
# Navigate to the project root
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

### 3. Verify Deployment

Check if the pods are running:

```powershell
kubectl get pods
```

Check the service:

```powershell
kubectl get service ai-text-analyzer-service
```

### 4. Access the Application

- **Via Port-Forwarding (Quickest for testing)**:
  ```powershell
  kubectl port-forward service/ai-text-analyzer-service 8080:80
  ```
  Then open `http://localhost:8080` in your browser.

- **Via Ingress**:
  Add `ai-analyzer.local` to your `/etc/hosts` (or `C:\Windows\System32\drivers\etc\hosts`) file:
  ```
  127.0.0.1 ai-analyzer.local
  ```
  (Replace `127.0.0.1` with your cluster's external IP or Minikube IP).
  Then visit `http://ai-analyzer.local`.

## Troubleshooting

- **ImagePullBackOff**: Ensure the image name in `deployment.yaml` matches your pushed image and that it is public (or use ImagePullSecrets).
- **CrashLoopBackOff**: Check pod logs: `kubectl logs <pod-name>`.
