# Video Presentation Guide

Main deck file:

`report/VIDEO_PRESENTATION.pptx`

Regenerate after edits:

```powershell
.\.venv312\Scripts\python.exe report\generate_presentation_pptx.py
```

---

## How to use during recording

1. Open the PPT in PowerPoint.
2. Insert screenshots into the blue placeholder boxes on each slide.
3. Use **Presenter View** (if available) to read speaker notes while recording.
4. Switch to terminal/browser live demos when the narration script says so.

---

## Screenshot placement map

| Slide | Insert this screenshot |
|-------|------------------------|
| Title | Optional: none |
| Agenda | Optional: none |
| Phase 0: Setup | VS Code project tree or README |
| Phase 1: Data and EDA | `screenshots/phase1_eda/class_balance.png` or all 3 EDA plots |
| Phase 2: Models | `report/generated/model_cv_metrics.csv` opened in editor |
| Model Comparison Results | Optional: confusion matrix from MLflow |
| Phase 3: MLflow | `screenshots/phase3_mlflow/02_run_training_table.png` |
| Phase 4: Packaging | `models/` folder or `model_metadata.json` |
| Phase 5: Tests and CI | `screenshots/Screenshot 2026-07-11 214818.png` |
| Phase 6: Docker | `screenshots/docker_run.png` + `screenshots/phase6_docker/03_curl_predict_success.png` |
| Phase 7: Kubernetes | `screenshots/phase7_k8s/k8s deployment.png` + `k8s health success.png` |
| Phase 8: Monitoring | `screenshots/phase8_monitoring/Request logs.png` + `metrics endpoint.png` |
| Architecture | Optional repo tree or draw diagram |
| Conclusion | Optional: none |

---

## Recording flow (recommended)

1. Show slide for the phase (30–45 sec)
2. Switch to live demo in VS Code/terminal/browser (45–90 sec)
3. Move to next slide

Pair this deck with:

- `report/VIDEO_NARRATION_SCRIPT.md` (what to say)
- `report/VIDEO_SCRIPT.md` (command checklist)
