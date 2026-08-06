from fastapi import FastAPI

from app.db import Base, engine
from app.models import models  # noqa: F401 — registra los modelos en Base.metadata
from app.routers import reading_router, sensor_router

app = FastAPI(title="SensorHub API", version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(sensor_router.router)
app.include_router(reading_router.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}