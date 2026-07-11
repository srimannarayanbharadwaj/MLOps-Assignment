# Video Narration Script (Read Aloud)

**Student:** Sriman Narayan Bharadwaj R  
**Length target:** 8–12 minutes  
**Tip:** Keep this file open on a second monitor or phone while you record.

Text in **[brackets]** = what to do on screen (don't read these aloud).  
Everything else = read naturally while demonstrating.

---

## OPENING

Hello, my name is **Sriman Narayan Bharadwaj R**.

This is my MLOps Assignment demo for the **Heart Disease prediction project**.

The goal of this project is to build a complete machine learning operations pipeline — from downloading medical data, training a model, tracking experiments, and finally deploying the model as an API using Docker and Kubernetes.

My GitHub repository is:
**github.com/srimannarayanbharadwaj/MLOps-Assignment**

Let me walk you through the entire pipeline end to end.

---

## SECTION 1 — PROJECT OVERVIEW

**[Show VS Code with the project folder open]**

Here is my project structure.

The `data` folder stores raw and processed datasets.

The `src` folder contains all Python scripts — for downloading data, cleaning, EDA, training, packaging, and the FastAPI service.

The `tests` folder has unit tests.

The `models` folder stores the final trained pipeline.

The `.github/workflows` folder contains the CI/CD pipeline.

And the `k8s` folder has Kubernetes deployment files for Minikube.

This structure keeps each MLOps stage separate and reproducible.

---

## SECTION 2 — ENVIRONMENT SETUP

**[Show terminal with (.venv312) active]**

First, I set up a Python 3.12 virtual environment, because MLflow UI did not work correctly on Python 3.14 on my machine.

I activate the environment and install dependencies from `requirements.txt`.

**[Optional: quickly show requirements.txt]**

All required packages are listed here — pandas, scikit-learn, mlflow, fastapi, pytest, and others.

---

## SECTION 3 — DATA DOWNLOAD AND CLEANING

**[Run in terminal:]**

```powershell
python -m src.data_download
```

I'm running the data download script now.

This fetches the **UCI Heart Disease dataset**, specifically the **Cleveland subset**, which has **303 patient records** and **13 clinical features**.

**[Show data/raw and data/processed folders]**

The raw file is saved in `data/raw`.

The cleaned file is saved here in `data/processed/heart_cleveland_clean.csv`.

During cleaning, missing values marked as question marks in columns like `ca` and `thal` are handled.

The target column is also converted to binary:
- **0** means no heart disease
- **1 or higher** is collapsed to **1**, meaning disease is present

After cleaning, we have **164 no-disease cases** and **139 disease cases**.

---

## SECTION 4 — EXPLORATORY DATA ANALYSIS

**[Run:]**

```powershell
python -m src.eda
```

**[Open screenshots/phase1_eda or the generated plots]**

Next, I generated three EDA plots.

First is the **class balance chart**. The dataset is slightly imbalanced, so accuracy alone is not enough — we also need precision, recall, and ROC-AUC.

Second are the **numeric feature histograms**. Features like age, cholesterol, and blood pressure have different scales, which is why we apply **StandardScaler** during modeling.

Third is the **correlation heatmap**. This shows which clinical features are more related to the target and helps explain model behavior.

These plots guided my preprocessing and model evaluation choices.

---

## SECTION 5 — MODEL TRAINING

**[Run:]**

```powershell
python -m src.train
```

Now I train and compare two models:
- **Logistic Regression**
- **Random Forest**

Both use the same preprocessing pipeline:
- numeric features are scaled
- categorical features are one-hot encoded

Evaluation uses **5-fold stratified cross-validation**.

**[Open report/generated/model_cv_metrics.csv]**

Here are the results.

Logistic Regression achieved:
- Accuracy: **0.8447**
- Precision: **0.8475**
- Recall: **0.8050**
- ROC-AUC: **0.9188**

Random Forest achieved:
- Accuracy: **0.8416**
- Precision: **0.8388**
- Recall: **0.8127**
- ROC-AUC: **0.9163**

I selected **Logistic Regression** for deployment because it has the best ROC-AUC.

Random Forest has slightly higher recall, but the difference is small, and Logistic Regression is simpler to explain and faster to serve in production.

---

## SECTION 6 — MLFLOW EXPERIMENT TRACKING

**[Run in a new terminal:]**

```powershell
mlflow ui
```

**[Open browser: http://127.0.0.1:5000]**

For experiment tracking, I used **MLflow**.

Each training run logs:
- model parameters
- cross-validation metrics
- confusion matrix images
- and the full sklearn pipeline as an artifact

**[Click experiment: heart-disease-classification]**

Here is my experiment called **heart-disease-classification**.

**[Open Training runs table]**

In the training runs table, I can compare Logistic Regression and Random Forest side by side.

**[Open one run → Artifacts tab]**

In the artifacts section, you can see the confusion matrix, metrics CSV, and the saved model.

MLflow makes experiment comparison much easier than manually checking separate output files.

**[Stop MLflow with Ctrl+C when done showing it]**

---

## SECTION 7 — MODEL PACKAGING

**[Run:]**

```powershell
python -m src.package_model
```

**[Show models/ folder]**

Next, I package the selected model into a single artifact.

This file — `heart_disease_pipeline.joblib` — contains both preprocessing and the trained Logistic Regression model.

I also save `model_metadata.json` with feature names, training row count, and CV metrics.

And `sample_input.json` is included for API testing.

This means a fresh clone of the repository can reproduce the packaged model using only `requirements.txt` and the packaging script.

---

## SECTION 8 — UNIT TESTS AND CI/CD

**[Run:]**

```powershell
pytest -q
flake8 src tests
```

I added automated tests to protect data cleaning and model behavior.

`test_data.py` checks null handling and target binarization.

`test_model.py` checks that predictions are binary and probabilities are valid.

`test_api.py` checks the `/health` and `/metrics` endpoints.

**[Open GitHub Actions in browser]**

On GitHub Actions, the CI pipeline runs three jobs in order:
1. Lint with flake8
2. Unit tests with pytest
3. Training and packaging script

**[Show green workflow run]**

This green run confirms the project is reproducible and passes quality checks automatically on each push.

---

## SECTION 9 — DOCKER CONTAINERIZATION

**[Run:]**

```powershell
docker build -t heart-disease-api:latest .
docker run --rm -p 8090:8000 heart-disease-api:latest
```

Now I containerize the FastAPI service using Docker.

The Dockerfile uses Python 3.12, installs dependencies, copies the source code and model, and starts uvicorn on port 8000.

**[In second terminal:]**

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8090/health -Method Get
```

The health endpoint confirms the service is running and the model is loaded.

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8090/predict `
  -Method Post `
  -ContentType "application/json" `
  -InFile api_sample_request.json
```

And here is a live prediction.

The API returns the predicted class, confidence score, risk label, and model name.

**[Stop Docker container with Ctrl+C]**

---

## SECTION 10 — KUBERNETES DEPLOYMENT (MINIKUBE)

**[Run:]**

```powershell
minikube start
minikube image load heart-disease-api:latest
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
```

For deployment, I used **Minikube** to run a local Kubernetes cluster.

I load the Docker image into Minikube, then apply the deployment and service YAML files from the `k8s` folder.

**[Show pod Running 1/1]**

The pod status shows **Running** with **1/1 ready**.

**[Run in second terminal:]**

```powershell
kubectl port-forward service/heart-disease-api 8080:8000
```

I use port-forward to access the service locally.

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8080/health -Method Get
```

The health check succeeds, which means the model API is deployed correctly on Kubernetes.

---

## SECTION 11 — MONITORING

**[Run:]**

```powershell
uvicorn src.api:app --host 127.0.0.1 --port 8090
```

Finally, I added basic monitoring to the FastAPI app.

**[Send a few requests in second terminal]**

Each request is logged with:
- timestamp
- endpoint
- HTTP method
- status code
- and latency in milliseconds

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8090/metrics -Method Get
```

The `/metrics` endpoint exposes **Prometheus-format metrics**, including request counts and request duration histograms.

In a real production system, these logs and metrics would help detect slow endpoints, rising error rates, and service health issues.

**[Stop uvicorn with Ctrl+C]**

---

## CLOSING

To summarize, this project demonstrates a full MLOps lifecycle:

1. Data ingestion and cleaning  
2. Exploratory data analysis  
3. Model training and comparison  
4. MLflow experiment tracking  
5. Model packaging  
6. Automated testing and CI/CD  
7. Docker containerization  
8. Kubernetes deployment  
9. Request logging and metrics monitoring  

The final model is **Logistic Regression** with ROC-AUC **0.9188**, deployed as a reproducible API service.

Thank you for watching.

My repository link again is:
**github.com/srimannarayanbharadwaj/MLOps-Assignment**

---

## QUICK RECORDING TIPS

- Speak slightly slower than normal conversation
- Pause 1–2 seconds after each command before explaining output
- If a command takes time (Docker build, training), keep talking briefly about what it is doing
- If something fails live, show the fix calmly — that is acceptable in MLOps demos
- Recommended filename: `heart-disease-mlops-demo.mp4`
