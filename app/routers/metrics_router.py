from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.models import Alert, Reading, Sensor

router = APIRouter()


@router.get("/metrics", status_code=200)
def get_metrics(db: Session = Depends(get_db)) -> dict[str, Any]:  # noqa: B008
    total_sensors = db.scalar(select(func.count()).select_from(Sensor)) or 0
    total_readings = db.scalar(select(func.count()).select_from(Reading)) or 0
    total_alerts = db.scalar(select(func.count()).select_from(Alert)) or 0
    open_alerts = db.scalar(
        select(func.count()).select_from(Alert).where(Alert.status == "open")
    ) or 0

    return {
        "total_sensors": total_sensors,
        "total_readings": total_readings,
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
    }