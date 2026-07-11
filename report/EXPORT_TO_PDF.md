# How to Export the Final Report to PDF

The main report template is:

`report/FINAL_REPORT.md`

## Step 1 — Personalize the report

Open `FINAL_REPORT.md` and rewrite every section marked with:

- _[Your Name]_
- _[Write ... in your own words]_
- _Your interpretation_

Keep screenshots and metrics, but change the explanations so they reflect your understanding.

## Step 2 — Export options

### Option A: VS Code extension (easiest)

1. Install extension: **Markdown PDF**
2. Open `report/FINAL_REPORT.md`
3. Right-click → **Markdown PDF: Export (pdf)**
4. Save as `report/FINAL_REPORT.pdf`

### Option B: Pandoc (if installed)

```powershell
pandoc report/FINAL_REPORT.md -o report/FINAL_REPORT.pdf
```

### Option C: Copy to Word/Google Docs

1. Open `FINAL_REPORT.md` in VS Code preview or GitHub
2. Copy sections into Word/Google Docs
3. Insert screenshots manually for best formatting
4. Export as PDF

## Step 3 — Length check

Target: **~10 pages** including screenshots and architecture diagram.

If too short:

- Expand EDA interpretation (Phase 1)
- Expand model selection rationale (Phase 2)
- Add a "Challenges" paragraph with your real issues (Python 3.14, port conflicts, etc.)

If too long:

- Keep one screenshot per phase (not every duplicate MLflow run)

## Step 4 — Submit

Submit according to your course portal:

- `FINAL_REPORT.pdf`
- Video file
- GitHub repo link: https://github.com/srimannarayanbharadwaj/MLOps-Assignment
