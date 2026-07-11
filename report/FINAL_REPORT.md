# Heart Disease MLOps — Final Report

**Student:** _[Your Name]_  
**Course:** MLOps Assignment 01 (2026)  
**Repository:** https://github.com/srimannarayanbharadwaj/MLOps-Assignment  
**Date:** _[Submission Date]_

---

> **Important:** This file is a structured report template. Rewrite the
> explanation sections in your own words before submitting. Keep the technical
> facts, commands, and screenshots, but personalize the analysis and conclusions.

---

## 1. Executive Summary

_[Write 1 short paragraph in your own words. Suggested points to cover:]_

- Built an end-to-end MLOps pipeline for the UCI Cleveland Heart Disease dataset (303 rows).
- Compared Logistic Regression and Random Forest with stratified 5-fold CV.
- Selected **Logistic Regression** (ROC-AUC: **0.9188**) as the production model.
- Deployed the model through FastAPI, Docker, Minikube/Kubernetes, and added monitoring.

---

## 2. Project Setup

### 2.1 Environment

- Python version used: **3.12** (required for MLflow UI compatibility)
- Virtual environment: `.venv312`
- Key packages: pandas, scikit-learn, mlflow, fastapi, uvicorn, pytest, prometheus-client

### 2.2 Repository Structure

```text
heart-disease-mlops/
|-- data/raw, data/processed
|-- src/               # download, cleaning, EDA, training, API
|-- tests/             # unit tests
|-- models/            # packaged pipeline
|-- .github/workflows/ # CI pipeline
|-- k8s/               # deployment manifests
|-- screenshots/       # evidence from each phase
`-- report/            # final report and generated metrics
```

### 2.3 Reproduction Commands

```powershell
python -m venv .venv312
.\.venv312\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.data_download
python -m src.eda
python -m src.train
python -m src.package_model
```

---

## 3. Phase 1 — Data and EDA

### 3.1 Dataset

- Source: UCI Heart Disease dataset, Cleveland subset
- Raw rows: **303**
- Features: **13** clinical attributes + binary target
- Missing values: `?` in `ca` and `thal`, handled during cleaning
- Target encoding: original values `0` = no disease, `1+` collapsed to `1` = disease

### 3.2 Class Balance

- No disease (`0`): **164**
- Disease (`1`): **139**

**Screenshot:** `screenshots/phase1_eda/class_balance.png`

**Your interpretation (rewrite in your own words):**

- _What does the class balance tell you about model evaluation?_
- _Should we use accuracy alone, or also precision/recall/ROC-AUC?_

### 3.3 Feature Distributions

**Screenshot:** `screenshots/phase1_eda/numeric_feature_histograms.png`

**Your interpretation:**

- _Which numeric features look skewed or have unusual ranges?_
- _Does `age` look approximately normal or skewed?_
- _Any features that may need scaling? (We used StandardScaler.)_

### 3.4 Correlation Heatmap

**Screenshot:** `screenshots/phase1_eda/correlation_heatmap.png`

**Your interpretation:**

- _Which features correlate most strongly with the target?_
- _Are any input features highly correlated with each other (multicollinearity)?_
- _What might that mean for Logistic Regression vs tree models?_

---

## 4. Phase 2 — Feature Engineering and Modeling

### 4.1 Preprocessing Pipeline

- Numeric features (`age`, `trestbps`, `chol`, `thalach`, `oldpeak`): `StandardScaler`
- Categorical features (`sex`, `cp`, `fbs`, `restecg`, `exang`, `slope`, `ca`, `thal`): `OneHotEncoder`
- Combined using `ColumnTransformer` inside a sklearn `Pipeline`

### 4.2 Cross-Validation Results

| Model | Accuracy | Precision | Recall | ROC-AUC |
|-------|----------|-----------|--------|---------|
| Logistic Regression | 0.8447 | 0.8475 | 0.8050 | **0.9188** |
| Random Forest | 0.8416 | 0.8388 | **0.8127** | 0.9163 |

Source: `report/generated/model_cv_metrics.csv`

### 4.3 Model Selection Justification

_[Rewrite this section in your own words. Example argument you can adapt:]_

I selected **Logistic Regression** because it achieved the highest ROC-AUC
(**0.9188**), which measures ranking quality across decision thresholds. Random
Forest had slightly higher recall (**0.8127** vs **0.8050**), which is clinically
important because false negatives can be costly in screening. However, the recall
gap is small, and Logistic Regression is simpler to explain and faster to serve
in production.

---

## 5. Phase 3 — Experiment Tracking (MLflow)

### 5.1 What Was Logged

For each model run:

- Parameters: model type, hyperparameters, CV folds
- Metrics: accuracy, precision, recall, ROC-AUC (mean and std)
- Artifacts: confusion matrix image, metrics CSV, model selection summary, sklearn pipeline

### 5.2 MLflow UI Evidence

**Screenshots:**

- `screenshots/phase3_mlflow/01_experiments_page.png`
- `screenshots/phase3_mlflow/02_run_training_table.png`
- `screenshots/phase3_mlflow/04_logistic_artifacts.png`

**Your summary (rewrite):**

- _What did MLflow help you compare quickly?_
- _Which run did you choose as best and why?_

---

## 6. Phase 4 — Packaging

### 6.1 Saved Artifacts

- `models/heart_disease_pipeline.joblib` — full preprocessing + model pipeline
- `models/model_metadata.json` — feature lists, training rows, CV metrics
- `models/sample_input.json` — sample inference payload
- `requirements.txt` — pinned dependencies for reproducibility

### 6.2 Reproducibility Check

From a fresh clone:

```powershell
pip install -r requirements.txt
python -m src.package_model
```

The packaged model should load and predict on `models/sample_input.json`.

---

## 7. Phase 5 — Unit Tests and CI/CD

### 7.1 Tests

- `tests/test_data.py` — null handling and target binarization
- `tests/test_model.py` — prediction shape, binary labels, valid probabilities
- `tests/test_api.py` — `/health` and `/metrics` endpoints

### 7.2 GitHub Actions Workflow

Jobs (fail-fast order):

1. **Lint** — flake8 on `src/` and `tests/`
2. **Unit Tests** — pytest
3. **Training Script** — data download, train, package model

**Screenshot:** `screenshots/Screenshot 2026-07-11 214818.png`

**Your summary:**

- _Why is CI useful in an MLOps project?_
- _What would break if someone changed cleaning logic without tests?_

---

## 8. Phase 6 — Containerization (Docker + FastAPI)

### 8.1 API Endpoints

- `GET /health` — service health and model metadata
- `POST /predict` — returns prediction, confidence, risk label
- `GET /metrics` — Prometheus metrics (Phase 8)

### 8.2 Docker Evidence

**Screenshots:**

- `screenshots/docker_run.png`
- `screenshots/phase6_docker/03_curl_predict_success.png`

Sample response from `/predict`:

```json
{
  "prediction": 0,
  "confidence": 0.8292,
  "risk_label": "no_disease",
  "model_name": "logistic_regression"
}
```

---

## 9. Phase 7 — Kubernetes Deployment (Minikube)

### 9.1 Manifests

- `k8s/deployment.yaml` — API deployment with readiness/liveness probes on `/health`
- `k8s/service.yaml` — NodePort service exposing port 8000

### 9.2 Deployment Steps

```powershell
minikube start
docker build -t heart-disease-api:latest .
minikube image load heart-disease-api:latest
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
kubectl port-forward service/heart-disease-api 8080:8000
```

**Screenshots:**

- `screenshots/phase7_k8s/minicube start success.png`
- `screenshots/phase7_k8s/k8s deployment.png`
- `screenshots/phase7_k8s/k8s port-forward.png`
- `screenshots/phase7_k8s/k8s health success.png`

---

## 10. Phase 8 — Monitoring

### 10.1 Request Logging

Middleware logs:

- timestamp (UTC)
- endpoint
- HTTP method
- status code
- latency in milliseconds

**Screenshot:** `screenshots/phase8_monitoring/Request logs.png`

### 10.2 Prometheus Metrics

`/metrics` exposes:

- `http_requests_total{method, endpoint, status_code}`
- `http_request_duration_seconds{method, endpoint}`

**Screenshot:** `screenshots/phase8_monitoring/metrics endpoint.png`

**Your summary:**

- _How would these logs/metrics help in production troubleshooting?_
- _What alert might you set on latency or error rate?_

---

## 11. System Architecture

```mermaid
flowchart LR
    A[UCI Heart Disease CSV] --> B[src/data_download.py]
    B --> C[data/processed/clean CSV]
    C --> D[src/eda.py + notebooks]
    C --> E[src/train.py]
    E --> F[MLflow Tracking]
    E --> G[report/generated metrics]
    E --> H[src/package_model.py]
    H --> I[models/heart_disease_pipeline.joblib]
    I --> J[FastAPI src/api.py]
    J --> K[Docker Image]
    K --> L[Minikube Deployment]
    L --> M[/predict /health /metrics]
    N[GitHub Actions CI] --> B
    N --> E
    N --> H
    O[pytest tests] --> N
```

---

## 12. Challenges and Lessons Learned

_[Write 3–5 bullets in your own words. Examples you can adapt:]_

- Python 3.14 broke MLflow UI; switching to Python 3.12 fixed it.
- Docker/Minikube port conflicts required using alternate ports or stopping old tunnels.
- Pinning `requirements.txt` made clean-clone reproduction reliable.
- MLflow made model comparison much faster than reading CSV files manually.

---

## 13. Conclusion

_[Short closing paragraph in your own words.]_

This project implemented a complete MLOps lifecycle: data ingestion, EDA,
model training, experiment tracking, packaging, automated testing, containerized
serving, Kubernetes deployment, and basic observability. The final Logistic
Regression pipeline achieved strong cross-validated performance and was deployed
as a reproducible API service.

---

## Appendix A — Repository Link

https://github.com/srimannarayanbharadwaj/MLOps-Assignment

## Appendix B — Video Demonstration

_[Add your video link or filename here after recording.]_

See `report/VIDEO_SCRIPT.md` for the recording checklist.
