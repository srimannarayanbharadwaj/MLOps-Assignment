# Heart Disease MLOps

End-to-end MLOps assignment project for the UCI Heart Disease dataset.

## Project Structure

```text
heart-disease-mlops/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── tests/
├── .github/workflows/
├── k8s/
├── screenshots/
└── report/
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

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

