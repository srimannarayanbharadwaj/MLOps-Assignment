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
2. Screenshots are already embedded on the phase slides.
3. Use **Presenter View** (if available) to read speaker notes while recording.
4. Switch to terminal/browser live demos when the narration script says so.

Regenerate with screenshots:

```powershell
.\.venv312\Scripts\python.exe report\generate_presentation_pptx.py
```

---

## Embedded screenshot map

| Slide | Screenshots embedded |
|-------|----------------------|
| Phase 0: Setup | MLflow experiments page |
| Phase 1: Data and EDA | class balance, histograms, heatmap |
| Phase 2: Models | MLflow training runs table |
| Model Comparison Results | MLflow logreg metrics + artifacts |
| Phase 3: MLflow | experiments page + training runs |
| Phase 4: Packaging | MLflow artifacts |
| Phase 5: Tests and CI | GitHub Actions green workflow |
| Phase 6: Docker | docker run + predict response |
| Phase 7: Kubernetes | minikube start + deployment + health |
| Phase 8: Monitoring | request logs + metrics endpoint |
| Architecture | MLflow experiments + k8s deployment |

---

## Recording flow (recommended)

1. Show slide for the phase (30–45 sec)
2. Switch to live demo in VS Code/terminal/browser (45–90 sec)
3. Move to next slide

Pair this deck with:

- `report/VIDEO_NARRATION_SCRIPT.md` (what to say)
- `report/VIDEO_SCRIPT.md` (command checklist)
