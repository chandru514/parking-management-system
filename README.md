# Parking Management System

**Student Name:** Chandru  
**Registration Number:** `24MIS0514`  
**Course:** Agile Development Process and DevOps Lab  

---

## 📌 Project Overview

The **Parking Management System** is an automated web-based solution for tracking vehicle entry, exit, parking durations, fee computations, and comprehensive historical records.

The application has been architected and developed across **three distinct progressive versions (v1, v2, v3)** in compliance with the DevOps laboratory requirements:

| Version | Feature | Description | Local Port | NodePort |
| :--- | :--- | :--- | :--- | :--- |
| **v1** | **Add Vehicle** | Record vehicle entry with timestamp, vehicle plate number, and vehicle type. | `5001` | `30001` |
| **v2** | **Exit Vehicle** | Record vehicle exit time, calculate parking duration, and compute billing fee. | `5002` | `30002` |
| **v3** | **View Records** | Comprehensive historical records dashboard with search, filtering, and analytics. | `5003` | `30003` |

---

## 📂 Repository Structure

```text
├── v1/
│   ├── app.py                # Version 1 Flask Application (Entry recording)
│   └── Dockerfile            # Docker configuration for v1
├── v2/
│   ├── app.py                # Version 2 Flask Application (Exit & Fee calculation)
│   └── Dockerfile            # Docker configuration for v2
├── v3/
│   ├── app.py                # Version 3 Flask Application (History & Dashboard)
│   └── Dockerfile            # Docker configuration for v3
├── k8s/
│   ├── v1-deployment.yaml    # Kubernetes Deployment & NodePort Service for v1
│   ├── v2-deployment.yaml    # Kubernetes Deployment & NodePort Service for v2
│   └── v3-deployment.yaml    # Kubernetes Deployment & NodePort Service for v3
├── app.py                    # Root entrypoint (launches complete v3 application)
├── Jenkinsfile               # Declarative Jenkins CI/CD Pipeline
├── requirements.txt          # Python dependencies
└── README.md                 # Complete documentation
```

---

## 🚀 Running Locally via Python (VS Code)

To test any version locally on your machine without Docker:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Individual Versions
* **Run Version 1** (Port 5001):
  ```bash
  python v1/app.py
  ```
  Open browser: [http://localhost:5001](http://localhost:5001)

* **Run Version 2** (Port 5002):
  ```bash
  python v2/app.py
  ```
  Open browser: [http://localhost:5002](http://localhost:5002)

* **Run Version 3** (Port 5003):
  ```bash
  python v3/app.py
  ```
  Open browser: [http://localhost:5003](http://localhost:5003)

---

## 🐳 Docker Containerization

Each version is isolated with its dedicated Dockerfile and tagged appropriately:

### Build Images
```bash
docker build -t chandru514/parking-system:v1 -f v1/Dockerfile .
docker build -t chandru514/parking-system:v2 -f v2/Dockerfile .
docker build -t chandru514/parking-system:v3 -f v3/Dockerfile .
```

### Run Containers Simultaneously
```bash
# Run v1 on port 5001
docker run -d -p 5001:5001 --name parking-v1 chandru514/parking-system:v1

# Run v2 on port 5002
docker run -d -p 5002:5002 --name parking-v2 chandru514/parking-system:v2

# Run v3 on port 5003
docker run -d -p 5003:5003 --name parking-v3 chandru514/parking-system:v3
```

### Push to DockerHub
```bash
docker login
docker push chandru514/parking-system:v1
docker push chandru514/parking-system:v2
docker push chandru514/parking-system:v3
```

---

## ☸️ Kubernetes Deployment

Deploy all 3 versions as separate Deployments and Services:

### Apply Kubernetes Manifests
```bash
kubectl apply -f k8s/v1-deployment.yaml
kubectl apply -f k8s/v2-deployment.yaml
kubectl apply -f k8s/v3-deployment.yaml
```

### Verify Deployment Status
```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

### Access Services Locally
* **NodePort Access**:
  * Version 1: `http://localhost:30001`
  * Version 2: `http://localhost:30002`
  * Version 3: `http://localhost:30003`

* **Port Forwarding (Alternative)**:
  ```bash
  kubectl port-forward svc/parking-service-v1 5001:5001
  kubectl port-forward svc/parking-service-v2 5002:5002
  kubectl port-forward svc/parking-service-v3 5003:5003
  ```

---

## ⚙️ Jenkins CI/CD Pipeline

The included `Jenkinsfile` automates:
1. **Source Code Checkout** from GitHub.
2. **Lint & Code Integrity Check** using `py_compile`.
3. **Docker Image Build** for tags `v1`, `v2`, and `v3`.
4. **DockerHub Push** with credentials.
5. **Kubernetes Rollout** across all 3 deployments.
6. **Rollout Verification** checking pod status.

### Jenkins Pipeline Setup:
1. Open Jenkins Dashboard -> **New Item** -> **Pipeline**.
2. Under **Pipeline Definition**, select **Pipeline script from SCM**.
3. SCM: **Git** -> Enter your GitHub Repository URL.
4. Add credential ID: `dockerhub-credentials` (DockerHub Username & Password/Token).
5. Script Path: `Jenkinsfile`.
6. Click **Save** and **Build Now**.

---

## 🌿 Git Branches & History

The repository maintains dedicated branches to showcase progressive version evolution:
* `v1`: Version 1 code & entry feature.
* `v2`: Version 2 code & exit feature.
* `v3`: Version 3 code & history analytics.
* `main`: Complete unified project and deployment automation.
