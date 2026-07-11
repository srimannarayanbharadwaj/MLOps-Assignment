# Phase 6 Docker / FastAPI Screenshots

Capture these after building and running the container locally.

## Required screenshots

1. `01_docker_build_success.png`
   - Terminal output from `docker build -t heart-disease-api:latest .`

2. `02_docker_run_success.png`
   - Terminal output from `docker run --rm -p 8000:8000 heart-disease-api:latest`

3. `03_curl_predict_success.png`
   - Successful `/predict` response from the running container

## Commands

```powershell
docker build -t heart-disease-api:latest .
docker run --rm -p 8000:8000 heart-disease-api:latest
```

In a second terminal:

```powershell
Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/predict `
  -Method Post `
  -ContentType "application/json" `
  -InFile api_sample_request.json
```

Optional health check:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/health -Method Get
```
