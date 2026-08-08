from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.reading_repo import SQLAlchemyReadingRepository
from app.schemas.reading_schema import ReadingCreate, ReadingOut, ReadingUpdate
from app.services.exceptions import ReadingNotFoundError, SensorNotFoundError
from app.services.reading_service import ReadingService

router = APIRouter()


def get_service(db: Session = Depends(get_db)) -> ReadingService:  # noqa: B008
    repo = SQLAlchemyReadingRepository(db)
    return ReadingService(repo=repo)


@router.get("/sensors/{id}/readings", response_model=list[ReadingOut], status_code=200)
def list_readings(
    id: int,
    limit: int = 50,
    offset: int = 0,
    from_date: str | None = Query(None, alias="from"),
    to_date: str | None = Query(None, alias="to"),
    service: ReadingService = Depends(get_service),  # noqa: B008
) -> Any:
    try:
        return service.list_for_sensor(
            sensor_id=str(id),
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from None


@router.post("/sensors/{id}/readings", response_model=ReadingOut, status_code=201)
def create_reading(
    id: int,
    reading: ReadingCreate,
    service: ReadingService = Depends(get_service),  # noqa: B008
) -> Any:
    try:
        return service.record(sensor_id=str(id), value=reading.value, unit=reading.unit)
    except SensorNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from None


@router.get("/readings/{id}", response_model=ReadingOut, status_code=200)
def get_reading(id: int, service: ReadingService = Depends(get_service)) -> Any:  # noqa: B008
    try:
        return service.get_reading(id)
    except ReadingNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None


@router.patch("/readings/{id}", response_model=ReadingOut, status_code=200)
def update_reading(
    id: int,
    patch_data: ReadingUpdate,
    service: ReadingService = Depends(get_service),  # noqa: B008
) -> Any:
    try:
        return service.update_reading(id, value=patch_data.value, unit=patch_data.unit)
    except ReadingNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from None


@router.delete("/readings/{id}", status_code=204)
def delete_reading(id: int, service: ReadingService = Depends(get_service)) -> None:  # noqa: B008
    try:
        service.delete_reading(id)
    except ReadingNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from None