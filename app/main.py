from fastapi import FastAPI

from app.db import Base, engine

# Importamos ambos routers
from app.routers import reading_router, sensor_router

# Nos aseguramos de que las tablas existan
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="1.0.0")

# ¡Conectamos las dos piezas del CRUD!
app.include_router(sensor_router.router)
app.include_router(reading_router.router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "db": "connected"}