# Kubernetes Deployment Guide

## Prerequisites

- Kubernetes cluster
- kubectl
- helm

## Deployment Steps

### Add Helm repositories:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

### Install PostgreSQL:

```bash
helm install postgres bitnami/postgresql
```

### Apply Kubernetes manifests:

```bash
kubectl apply -f k8s/
```

## Manifest Structure

```yaml
matchai/
└── k8s/
    ├── backend/
    │   ├── deployment.yaml
    │   └── service.yaml
    ├── frontend/
    │   ├── deployment.yaml
    │   └── service.yaml
    └── ingress.yaml
```
