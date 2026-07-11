# Phase 8 Monitoring Screenshots

Capture these after starting the API locally.

## Required screenshots

1. `01_request_logs.png`
   - Terminal showing request log lines with timestamp, endpoint, and latency

2. `02_metrics_endpoint.png`
   - `/metrics` response showing Prometheus text metrics

## Commands

Start the API:

```powershell
uvicorn src.api:app --host 127.0.0.1 --port 8080
```

In a second terminal, send a few requests:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8080/health -Method Get
Invoke-RestMethod `
  -Uri http://127.0.0.1:8080/predict `
  -Method Post `
  -ContentType "application/json" `
  -InFile api_sample_request.json
```

Open metrics in browser or terminal:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8080/metrics -Method Get
```

You should see log lines like:

```text
timestamp=... endpoint=/health method=GET status=200 latency_ms=...
```

And metrics like:

```text
http_requests_total{endpoint="/health",method="GET",status_code="200"} 1.0
```
