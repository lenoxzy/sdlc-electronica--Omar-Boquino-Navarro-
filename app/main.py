from fastapi import FastAPI

from app.routers import alert_router, reading_router, sensor_router

app = FastAPI(title="SensorHub API", version="0.1.1") # cambio de version 

app.include_router(sensor_router.router)
app.include_router(reading_router.router)
app.include_router(alert_router.router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}