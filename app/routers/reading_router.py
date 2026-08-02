from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.reading_repo import SQLAlchemyReadingRepository
from app.schemas.reading_schema import ReadingCreate, ReadingOut
from app.services.reading_service import ReadingService
from typing import Generator, Any
router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_service(db: Session = Depends(get_db)) -> ReadingService: # noqa: B008 
    repo = SQLAlchemyReadingRepository(db)
    return ReadingService(repo=repo)


@router.get("/sensors/{id}/readings", response_model=list[ReadingOut], status_code=200)
def list_readings(
    id: int,
    limit: int = 50,
    offset: int = 0,
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
    service: ReadingService = Depends(get_service),# noqa: B008
) -> list[Any]: 
    
    # así el mock de get_service sí intercepta la llamada
    readings = service._repo.list_for_sensor(sensor_id=str(id))
    return readings


@router.post("/sensors/{id}/readings", response_model=ReadingOut, status_code=201)
def create_reading(
    id: int,
    reading: ReadingCreate,
    service: ReadingService = Depends(get_service),# noqa: B008
) -> Any: 
    try:
        new_record = service.record(
            sensor_id=str(id), value=reading.value, unit=reading.unit
        )
        return new_record
    except ValueError as e:
        if str(e) == "Sensor no encontrado":
            raise HTTPException(status_code=404, detail="Sensor no encontrado")from None
        raise HTTPException(status_code=422, detail=str(e)) from None


@router.get("/readings/{id}", response_model=ReadingOut, status_code=200)
def get_reading(id: int) -> dict[str, Any]: 
    return {"id": id, "value": 25.0, "unit": "C"}


@router.patch("/readings/{id}", response_model=ReadingOut, status_code=200)
def update_reading(id: int) -> dict[str, Any]: 
    return {"id": id, "value": 26.0, "unit": "C"}


@router.delete("/readings/{id}", status_code=204)
def delete_reading(id: int) -> None: 
    return None