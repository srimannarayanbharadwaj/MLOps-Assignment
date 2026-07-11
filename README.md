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
