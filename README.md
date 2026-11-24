# Swaraj Kumar Padhi — Portfolio Backend (FastAPI)

Lightweight Python FastAPI backend with SQLite persistence for your GitHub Pages portfolio (`https://igvenom202.github.io/swaraj_motion_portfolio.github.io/`).

## Endpoints
- `GET /api/health` — Health & uptime check
- `GET /api/metrics` — Solar EPC capacity metrics (35 MW utility + 5 MW pump EPC = 40 MW total)
- `GET /api/missions?category=epc|data|ai` — Filterable portfolio missions
- `POST /api/contact` — Saves contact form inquiries (`name`, `email`, `topic`, `message`) to SQLite
- `GET /api/inquiries` — Lists saved inquiries (requires `X-API-Key` header matching `ADMIN_API_KEY`)

## Run Locally
```bash
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## Deploy (Render / Railway)
1. Push this folder (`app.py`, `requirements.txt`, `.env.example`) to a GitHub repository.
2. Create a new **Web Service** on Render or Railway.
3. Set Build Command: `pip install -r requirements.txt`
4. Set Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add environment variable `ADMIN_API_KEY` and `ALLOWED_ORIGINS=https://igvenom202.github.io`.
6. Copy your deployed HTTPS URL (e.g. `https://swaraj-portfolio-api.onrender.com`) into `API_BASE_URL` inside `index.html`.
