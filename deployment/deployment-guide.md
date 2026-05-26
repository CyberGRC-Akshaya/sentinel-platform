# Sentinel v1.2 Deployment Guide

## Goal

Create public demo URLs for:
1. Static Sentinel landing page
2. Sentinel frontend
3. Sentinel backend API

## Fastest public landing page

Use Netlify Drop for:

```text
website/index.html
```

Steps:
1. Open Netlify Drop.
2. Drag the `website` folder.
3. Copy the public URL.
4. Add it to GitHub README and LinkedIn.

## Backend API on Render

Render settings:

| Field | Value |
|---|---|
| Service Type | Web Service |
| Runtime | Python |
| Build Command | `cd backend && pip install -r requirements.txt` |
| Start Command | `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

Test after deployment:

```text
https://your-service-name.onrender.com/api/health
```

## Frontend on Vercel

Vercel settings:

| Field | Value |
|---|---|
| Framework | Next.js |
| Root Directory | `frontend` |
| Environment Variable | `NEXT_PUBLIC_API_URL=https://your-render-backend-url.onrender.com` |

Local Docker fallback remains:

```text
http://localhost:8000
```
