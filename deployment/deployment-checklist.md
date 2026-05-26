# Sentinel Deployment Checklist

## Before deployment

- [ ] GitHub repo pushed
- [ ] App runs locally
- [ ] Backend health works locally
- [ ] v1.2 fixed patch applied
- [ ] README has public demo URL section

## Landing page

- [ ] Deploy `website` folder to Netlify Drop
- [ ] Copy URL

## Backend

- [ ] Create Render Web Service
- [ ] Connect GitHub repo
- [ ] Build command: `cd backend && pip install -r requirements.txt`
- [ ] Start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Test `/api/health`

## Frontend

- [ ] Create Vercel project
- [ ] Root directory: `frontend`
- [ ] Add env var `NEXT_PUBLIC_API_URL`
- [ ] Deploy
- [ ] Run Examiner Review on deployed frontend
