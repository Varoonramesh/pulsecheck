from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import requests
import time

from app.database import Base, engine, get_db
from app.models import URLMonitor
from app.schemas import URLCreate, URLResponse

app = FastAPI(title="PulseCheck API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def check_url(monitor: URLMonitor):
    try:
        start = time.perf_counter()

        response = requests.get(
            monitor.url,
            timeout=5,
            allow_redirects=True,
        )

        elapsed = (time.perf_counter() - start) * 1000

        monitor.status = "UP"
        monitor.status_code = response.status_code
        monitor.response_time_ms = round(elapsed, 2)
        monitor.checked_at = datetime.utcnow()

    except Exception:
        monitor.status = "DOWN"
        monitor.status_code = None
        monitor.response_time_ms = None
        monitor.checked_at = datetime.utcnow()


@app.get("/")
def root():
    return {"message": "PulseCheck API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/urls", response_model=list[URLResponse])
def list_urls(db: Session = Depends(get_db)):
    urls = db.query(URLMonitor).all()

    for url in urls:
        check_url(url)

    db.commit()

    return urls


@app.post("/api/urls", response_model=URLResponse)
def create_url(payload: URLCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(URLMonitor)
        .filter(URLMonitor.url == str(payload.url))
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="URL already exists",
        )

    monitor = URLMonitor(
        url=str(payload.url)
    )

    db.add(monitor)
    db.commit()

    check_url(monitor)

    db.commit()
    db.refresh(monitor)

    return monitor


@app.delete("/api/urls/{url_id}")
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
):
    item = (
        db.query(URLMonitor)
        .filter(URLMonitor.id == url_id)
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="URL not found",
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Deleted successfully"
    }
