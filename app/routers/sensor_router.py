
from collections.abc import Generator
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.sensor_repo import SQLAlchemySensorRepository
from app.schemas.sensor_schema import SensorCreate, SensorOut
from app.services.sensor_service import SensorService

router = APIRouter()

def get_db() -> Generator[Session, None, None]: 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sensor_service(db: Session = Depends(get_db)) -> SensorService: # noqa: B008 <-- Devuelve tu clase servicio
    repo = SQLAlchemySensorRepository(db)
    return SensorService(repo=repo)

@router.get("/sensors/{id}", response_model=SensorOut, status_code=200)
def get_sensor(id: int, service: SensorService = Depends(get_sensor_service)) -> Any:  # noqa: B008
    try:
        return service.get_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None

@router.post("/sensors", response_model=SensorOut, status_code=201)
def create_sensor(
    sensor: SensorCreate, 
    service: SensorService = Depends(get_sensor_service),  # noqa: B008
) -> Any:
    return service.create(sensor) 

@router.delete("/sensors/{id}", status_code=204)
def delete_sensor(id: int, service: SensorService = Depends(get_sensor_service)) -> None:  # noqa: B008
    try:
        service.delete(id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None

@router.get("/sensors", response_model=list[SensorOut], status_code=200)
def list_sensors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: SensorService = Depends(get_sensor_service),  # noqa: B008
) -> Any:
    return service.get_all(skip=skip, limit=limit)