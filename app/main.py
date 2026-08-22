from fastapi import FastAPI

from app.core.logging_config import configure_logging
from app.routers import alert_router, metrics_router, reading_router, sensor_router

configure_logging()



app = FastAPI(title="SensorHub API", version="0.1.1")

app.include_router(sensor_router.router)
app.include_router(reading_router.router)
app.include_router(alert_router.router)
app.include_router(metrics_router.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}