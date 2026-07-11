# End-to-End Video Walkthrough Script

Record yourself running the pipeline in your own voice. Aim for **8–12 minutes**.
Show your face or at least your screen + voice clearly.

---

## Before Recording

- [ ] Close unnecessary apps (Docker Desktop and Minikube can stay open)
- [ ] Activate `.venv312`
- [ ] Repo path: `D:\MLOps\heart-disease-mlops`
- [ ] Have `api_sample_request.json` ready

Suggested recording tools: OBS Studio, Xbox Game Bar (`Win+G`), or Zoom screen record.

---

## Script (in order)

### 1. Introduction (30 sec)

Say:

- Your name
- Assignment title: Heart Disease MLOps
- GitHub repo link
- One sentence on goal: predict heart disease risk and deploy with MLOps tooling

---

### 2. Project Overview (45 sec)

Show in VS Code:

- `src/`, `tests/`, `models/`, `k8s/`, `.github/workflows/`
- Briefly explain each folder's role

---

### 3. Data Download and Cleaning (1 min)

```powershell
.\.venv312\Scripts\Activate.ps1
python -m src.data_download
```

Show:

- `data/raw/processed.cleveland.data`
- `data/processed/heart_cleveland_clean.csv`
- Mention: 303 rows, missing `?` handled, binary target

---

### 4. EDA (1 min)

Open screenshots or regenerate:

```powershell
python -m src.eda
```

Show and explain in your own words:

- class balance plot
- histograms
- correlation heatmap

---

### 5. Model Training (1 min)

```powershell
python -m src.train
```

Show:

- `report/generated/model_cv_metrics.csv`
- Say which model you picked and why (Logistic Regression, ROC-AUC 0.9188)

---

### 6. MLflow (1 min)

```powershell
mlflow ui
```

Open http://127.0.0.1:5000

Show:

- experiment `heart-disease-classification`
- Training runs comparison
- artifacts (confusion matrix, logged model)

Stop MLflow UI with `Ctrl+C` when done.

---

### 7. Packaging (45 sec)

```powershell
python -m src.package_model
```

Show:

- `models/heart_disease_pipeline.joblib`
- `models/model_metadata.json`

---

### 8. Tests and CI (1 min)

```powershell
pytest -q
flake8 src tests
```

Open GitHub Actions in browser:

https://github.com/srimannarayanbharadwaj/MLOps-Assignment/actions

Show a green workflow run.

---

### 9. Docker API (1.5 min)

```powershell
docker build -t heart-disease-api:latest .
docker run --rm -p 8090:8000 heart-disease-api:latest
```

Second terminal:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8090/health -Method Get
Invoke-RestMethod `
  -Uri http://127.0.0.1:8090/predict `
  -Method Post `
  -ContentType "application/json" `
  -InFile api_sample_request.json
```

Stop container with `Ctrl+C`.

---

### 10. Kubernetes (1.5 min)

```powershell
minikube start
minikube image load heart-disease-api:latest
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
kubectl port-forward service/heart-disease-api 8080:8000
```

Second terminal:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8080/health -Method Get
```

Show pod status `Running 1/1`.

---

### 11. Monitoring (1 min)

```powershell
uvicorn src.api:app --host 127.0.0.1 --port 8090
```

Send 2–3 requests, then show:

- request logs in terminal
- `/metrics` endpoint output

---

### 12. Closing (30 sec)

Summarize:

- Full pipeline from raw data to deployed API
- Repo link again
- Thank you / end

---

## Submission Checklist

- [ ] Video shows all major phases
- [ ] Your voice explains steps (not silent screen recording only)
- [ ] GitHub repo link mentioned
- [ ] At least one live prediction demo included
- [ ] Video file named clearly, e.g. `heart-disease-mlops-demo.mp4`
- [ ] Upload video per course instructions (Drive/portal/LMS)
