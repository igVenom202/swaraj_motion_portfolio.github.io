import os
import sqlite3
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

DB_PATH = os.getenv("DB_PATH", "inquiries.db")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "change-me-in-production")
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "https://igvenom202.github.io,http://localhost:8000,http://127.0.0.1:5500",
).split(",")

app = FastAPI(
    title="Swaraj Kumar Padhi — Solar EPC Portfolio API",
    version="1.0.0",
    description="Backend API for Swaraj Kumar Padhi's Solar EPC & Data Automation Portfolio.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                topic TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


init_db()


class ContactInquiry(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: Optional[EmailStr] = None
    topic: str = Field(..., min_length=2, max_length=120)
    message: str = Field(..., min_length=5, max_length=3000)


METRICS = {
    "utility_solar_mw": 35,
    "serp_mw": 26,
    "mskpy_mw": 9,
    "pump_epc_mw": 5,
    "total_capacity_mw": 40,
    "pm_kusum_sites": 2843,
    "msedcl_sites": 1856,
    "meda_sites": 987,
    "workflows": ["B2B", "B2C", "B2G"],
}

MISSIONS = [
    {"index": "01", "category": "data", "title": "Solar EPC Project Tracking Dashboard", "year": "2026"},
    {"index": "02", "category": "ai", "title": "Solar EPC Tracking Automation Architecture", "year": "2026"},
    {"index": "03", "category": "epc", "title": "MSKPY (9 MW) & SERP (26 MW) Solar Plants", "year": "2026 - Present"},
    {"index": "04", "category": "epc", "title": "MSEDCL & MEDA PM-KUSUM Solar Pumps", "year": "2025 - 2026"},
    {"index": "05", "category": "data", "title": "Solar EPC Data Management & Reporting", "year": "2026"},
    {"index": "06", "category": "ai", "title": "AI-Assisted Project Intelligence Framework", "year": "2026"},
    {"index": "07", "category": "ai", "title": "Enterprise ERP Business Process Model", "year": "2026"},
]


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "swaraj-epc-portfolio-api", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/metrics")
def get_metrics():
    return METRICS


@app.get("/api/missions")
def get_missions(category: Optional[str] = Query(default=None, description="Filter by epc, data, or ai")):
    if category and category != "all":
        filtered = [m for m in MISSIONS if m["category"] == category.lower()]
        return {"count": len(filtered), "missions": filtered}
    return {"count": len(MISSIONS), "missions": MISSIONS}


@app.post("/api/contact", status_code=201)
def submit_inquiry(payload: ContactInquiry):
    created_at = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO inquiries (name, email, topic, message, created_at) VALUES (?, ?, ?, ?, ?)",
            (payload.name.strip(), str(payload.email) if payload.email else None, payload.topic.strip(), payload.message.strip(), created_at),
        )
        conn.commit()
        inquiry_id = cursor.lastrowid

    return {
        "status": "received",
        "id": inquiry_id,
        "created_at": created_at,
        "message": "Inquiry saved successfully.",
    }


@app.get("/api/inquiries")
def list_inquiries(x_api_key: Optional[str] = Header(default=None)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key header")
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, name, email, topic, message, created_at FROM inquiries ORDER BY id DESC"
        ).fetchall()
    return {"count": len(rows), "inquiries": [dict(row) for row in rows]}
