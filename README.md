# MLOps Assignment: Heart Disease MLOps

End-to-end MLOps assignment project for the UCI Heart Disease dataset.

## Project Structure

```text
heart-disease-mlops/
|-- data/
|   |-- raw/
|   `-- processed/
|-- notebooks/
|-- src/
|-- tests/
|-- .github/workflows/
|-- k8s/
|-- screenshots/
`-- report/
```

## Planned Workflow

1. Download and clean the Heart Disease UCI dataset.
2. Create EDA plots and document observations.
3. Train Logistic Regression and Random Forest pipelines.
4. Track experiments with MLflow.
5. Package the best model for FastAPI serving.
6. Add tests, CI, Docker, Kubernetes manifests, and monitoring.
7. Collect screenshots and write the final report.

## Setup

Use Python 3.12 for this project. Python 3.14 can run the training script,
but the MLflow UI may fail because some MLflow dependencies have not fully
caught up with Python 3.14 yet.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Reproduce The Pipeline

```powershell
python -m src.data_download
python -m src.eda
python -m src.train
python -m src.package_model
```

The final packaged model is saved at:

```text
models/heart_disease_pipeline.joblib
```

## Serve Locally

```powershell
uvicorn src.api:app --host 127.0.0.1 --port 8000
```

In a second terminal:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/predict `
  -Method Post `
  -ContentType "application/json" `
  -InFile api_sample_request.json
```

## Docker

```powershell
docker build -t heart-disease-api:latest .
docker run --rm -p 8000:8000 heart-disease-api:latest
```

Then test the running container:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/predict `
  -Method Post `
  -ContentType "application/json" `
  -InFile api_sample_request.json
```

## Kubernetes (Minikube)

Install Minikube and kubectl, then deploy the Docker image to a local cluster.

```powershell
minikube start
docker build -t heart-disease-api:latest .
minikube image load heart-disease-api:latest
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
minikube service heart-disease-api --url
```

Use the returned service URL to test the deployed API:

```powershell
Invoke-RestMethod `
  -Uri "<SERVICE_URL>/predict" `
  -Method Post `
  -ContentType "application/json" `
  -InFile api_sample_request.json
```

To remove the deployment:

```powershell
kubectl delete -f k8s/
minikube stop
```

## Monitoring

The API logs every request with timestamp, endpoint, method, status code,
and latency. Prometheus metrics are exposed at `/metrics`.

```powershell
uvicorn src.api:app --host 127.0.0.1 --port 8080
```

In a second terminal:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8080/health -Method Get
Invoke-RestMethod -Uri http://127.0.0.1:8080/metrics -Method Get
```

## Final Report and Video (Phase 9)

Report templates are in `report/`:

- `report/FINAL_REPORT.md` — personalize and export to PDF
- `report/VIDEO_SCRIPT.md` — end-to-end recording checklist
- `report/EXPORT_TO_PDF.md` — PDF export instructions

Repository: https://github.com/srimannarayanbharadwaj/MLOps-Assignment
