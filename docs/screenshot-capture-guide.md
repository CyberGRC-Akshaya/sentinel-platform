# Sentinel Screenshot Capture Guide

## Goal

Capture five clean screenshots for GitHub, LinkedIn, and demo packaging.

## Before capturing

Run Sentinel:

```powershell
cd $HOME\Desktop\EyeOnBits-Sentinel
docker compose up --build
```

Open:

```text
http://localhost:3000
```

Set browser zoom to 80% or 90% so the layout fits.

## Screenshots to capture

### 1. Home / Case Library

File name:

```text
github-assets/01-home-case-library.png
```

Capture:
- Sentinel Assurance Platform header
- v0.4/v0.6 console card
- Sample Case Library

### 2. IT Metrics Examiner Output

File name:

```text
github-assets/02-it-metrics-output.png
```

Steps:
- Select IT Metrics Examiner
- Click Run Examiner Review
- Capture assurance score, rating, severity distribution, and first finding

### 3. Vendor & Privacy Examiner Output

File name:

```text
github-assets/03-vendor-privacy-output.png
```

Steps:
- Select Vendor & Privacy Examiner
- Click Run Examiner Review
- Capture evidence gaps and findings

### 4. SDLC & AI Governance Examiner Output

File name:

```text
github-assets/04-sdlc-ai-output.png
```

Steps:
- Select SDLC & AI Governance Examiner
- Click Run Examiner Review
- Capture AI governance finding

### 5. HTML Report

File name:

```text
github-assets/05-html-report.png
```

Steps:
- Click Download HTML Report
- Open downloaded HTML file in browser
- Capture report top section and first finding

## Screenshot quality rules

- Use full browser width
- Hide personal bookmarks if possible
- Avoid showing unrelated desktop content
- Use consistent zoom
- Save PNG files only
