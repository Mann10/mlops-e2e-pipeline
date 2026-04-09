# MLOps End-to-End Pipeline

This project implements an end-to-end MLOps pipeline for an Iris classification model. It includes model training, a FastAPI-based inference service, containerization with Docker, deployment to Kubernetes using KServe, and CI/CD automation with GitHub Actions and ArgoCD.

## Features

- **Model Training**: Trains a RandomForest classifier on the Iris dataset and saves the model.
- **Inference API**: FastAPI application that loads the model and provides prediction endpoints.
- **Containerization**: Docker image for easy deployment.
- **Kubernetes Deployment**: Uses KServe for scalable ML model serving on Kubernetes.
- **CI/CD**: Automated testing, building, pushing images, and GitOps deployment via ArgoCD.

## KServe Overview

KServe is a Kubernetes-native model serving framework that simplifies the deployment and management of ML models. It provides features like auto-scaling, canary deployments, and integration with inference runtimes. In this project, KServe handles the InferenceService defined in `k8s/inference.yaml`, automatically managing pods and scaling based on traffic.

## Prerequisites

- [kind](https://kind.sigs.k8s.io/) for local Kubernetes cluster
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Helm](https://helm.sh/)
- Docker Hub account for image registry
- GitHub repository secrets: `DOCKERHUB_USERNAME` and `DOCKERHUB_PASSWORD`

## Setup

### 1. Create Kind Cluster

```bash
kind create cluster --name=mlops-cluster
kubectl config current-context
```

### 2. Install Cert-Manager

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
kubectl get pods -n cert-manager
```

### 3. Install KServe

```bash
kubectl create namespace kserve

helm upgrade -install kserve oci://ghcr.io/kserve/charts/kserve \
  --version v0.16.0 \
  -n kserve \
  --set kserve.controller.deploymentMode=RawDeployment \
  --wait
```

*Note: Run the Helm command multiple times if errors occur.*

### 4. Deploy Inference Service

```bash
kubectl apply -f k8s/inference.yaml
# This deploys to default namespace; you can use a separate namespace if preferred.
kubectl get svc
```

### 5. Install ArgoCD

```bash
kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl get pods -n argocd -w

# Access ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

### 6. Set Up ArgoCD Application

In the ArgoCD UI, create a new application pointing to this repository (e.g., https://github.com/Mann10/mlops-e2e-pipeline), targeting the `k8s/` directory, and set the destination namespace to `default` (or your chosen namespace).

## Manual Testing

For local testing with Kind:

```bash
kubectl port-forward svc/iris-model-predictor 8080:80
```

Then test the API:

```bash
curl --location 'http://localhost:8080/predict' \
--header 'Content-Type: application/json' \
--data '{"data": [0, 0, 0, 0]}'
```

*Note: For cloud deployments, configure load balancers (e.g., NGINX, ALB) and install the corresponding controllers.*

## CI/CD Pipeline

The project uses GitHub Actions for automated CI/CD:

- **CI Workflow** (`.github/workflows/ci.yml`): Triggers on pushes/PRs to `main`.
  - Lints code with flake8.
  - Trains the model and runs tests.
  - Builds and tests the Docker image.

- **CD Workflow** (`.github/workflows/cd.yml`): Triggers after successful CI.
  - Builds and pushes the Docker image to Docker Hub.
  - Updates the image tag in `k8s/inference.yaml`.
  - Commits and pushes changes, triggering ArgoCD to sync and deploy.

Ensure repository secrets are set for Docker Hub authentication.

## Project Structure

- `model/`: Model training script and saved model.
- `app/`: FastAPI inference application.
- `k8s/`: Kubernetes manifests for KServe.
- `tests/`: Unit tests for the app and model.
- `.github/workflows/`: CI/CD workflows.

## Usage

1. Train the model: `cd model && python train.py`
2. Run the app locally: `cd app && uvicorn main:app --reload`
3. Build Docker image: `docker build -t iris-model .`
4. Deploy via ArgoCD or manually with `kubectl apply -f k8s/inference.yaml`

For contributions, ensure tests pass and follow the CI/CD flow.</content>
<parameter name="filePath">C:\personal\mlops-e2e-pipeline\README.md