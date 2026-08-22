from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repo import SQLAlchemyAlertRepository
from app.schemas.alert_schema import AlertOut, AlertStatusUpdate

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


@router.patch("/alerts/{id}/status", response_model=AlertOut, status_code=200)
def update_alert_status(
    id: int,
    patch: AlertStatusUpdate,
    repo: SQLAlchemyAlertRepository = Depends(get_alert_repo),  # noqa: B008
) -> Any:
    try:
        updated = repo.update_status(id, patch.status)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from None
    if not updated:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return updated