# Model Artifacts

Generate the packaged model with:

```powershell
python -m src.package_model
```

Tracked Phase 4 outputs:

- `heart_disease_pipeline.joblib`: fitted preprocessing + classifier pipeline.
- `model_metadata.json`: training rows, feature names, selected metrics.
- `sample_input.json`: one valid request-style sample row for later API testing.

