# Phase 7 Kubernetes / Minikube Screenshots

Capture these after deploying the API to Minikube.

## Required screenshots

1. `01_minikube_start.png`
   - Output from `minikube start`

2. `02_kubectl_get_pods.png`
   - Pod status shows `Running` and `READY 1/1`

3. `03_kubectl_get_svc.png`
   - Service shows `heart-disease-api` with `NodePort`

4. `04_minikube_service_url.png`
   - Output from `minikube service heart-disease-api --url`

5. `05_curl_predict_success.png`
   - Successful `/predict` response through the Minikube service URL

## Commands

```powershell
minikube start
docker build -t heart-disease-api:latest .
minikube image load heart-disease-api:latest
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
minikube service heart-disease-api --url
```

Test prediction (replace `<SERVICE_URL>` with the URL from the previous command):

```powershell
Invoke-RestMethod `
  -Uri "<SERVICE_URL>/predict" `
  -Method Post `
  -ContentType "application/json" `
  -InFile api_sample_request.json
```
