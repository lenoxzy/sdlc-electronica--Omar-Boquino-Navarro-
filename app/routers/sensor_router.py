
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.sensor_repo import SQLAlchemySensorRepository
from app.schemas.sensor_schema import SensorCreate, SensorOut
from app.services.sensor_service import SensorService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sensor_service(db: Session = Depends(get_db)): # noqa: B008
    repo = SQLAlchemySensorRepository(db)
    return SensorService(repo=repo)

@router.get("/sensors", response_model=list[SensorOut], status_code=200)
def list_sensors(service: SensorService = Depends(get_sensor_service)):  # noqa: B008
    return service.get_all()

@router.get("/sensors/{id}", response_model=SensorOut, status_code=200)
def get_sensor(id: int, service: SensorService = Depends(get_sensor_service)):  # noqa: B008
    try:
        return service.get_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None

@router.post("/sensors", response_model=SensorOut, status_code=201)
def create_sensor(
    sensor: SensorCreate, 
    service: SensorService = Depends(get_sensor_service),  # noqa: B008
):
    return service.create(sensor) 

@router.delete("/sensors/{id}", status_code=204)
def delete_sensor(id: int, service: SensorService = Depends(get_sensor_service)):  # noqa: B008
    try:
        service.delete(id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None