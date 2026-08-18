from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repo import SQLAlchemyAlertRepository
from app.schemas.alert_schema import AlertOut

router = APIRouter()


def get_alert_repo(
    db: Session = Depends(get_db),  # noqa: B008
) -> SQLAlchemyAlertRepository:
    return SQLAlchemyAlertRepository(db)


@router.get("/alerts", response_model=list[AlertOut], status_code=200)
def list_alerts(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repo: SQLAlchemyAlertRepository = Depends(get_alert_repo),  # noqa: B008
) -> Any:
    return repo.list_all(limit=limit, offset=offset)


@router.get(
    "/sensors/{id}/alerts", response_model=list[AlertOut], status_code=200
)
def list_alerts_for_sensor(
    id: int,
    repo: SQLAlchemyAlertRepository = Depends(get_alert_repo),  # noqa: B008
) -> Any:
    return repo.list_for_sensor(id)