from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Reading, Sensor


# --- 1. MODELO DE DATOS (Lo que entiende la capa de negocio) ---
@dataclass
class ReadingModel:
    id: int
    sensor_id: str
    value: float
    unit: str


# --- 2. EL PROTOCOLO (Inversión de Dependencias) ---
class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]: ...
    def get(self, reading_id: int) -> ReadingModel | None: ...
    def update(
        self, reading_id: int, value: float | None = None, unit: str | None = None
    ) -> ReadingModel | None: ...
    def delete(self, reading_id: int) -> bool: ...


# --- 3. LA IMPLEMENTACIÓN REAL (Capa de Datos) ---
class SQLAlchemyReadingRepository:
    """Implementación real del repositorio usando SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        sensor = self.db.get(Sensor, int(sensor_id))
        if not sensor:
            raise ValueError("Sensor no encontrado")

        new_reading = Reading(value=value, unit=unit, sensor_id=sensor.id)
        self.db.add(new_reading)
        self.db.commit()
        self.db.refresh(new_reading)

        return self._to_model(new_reading)

    def list_for_sensor(
        self,
        sensor_id: str,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]:
        stmt = select(Reading).where(Reading.sensor_id == int(sensor_id))
        if from_date is not None:
            stmt = stmt.where(Reading.created_at >= from_date)
        if to_date is not None:
            stmt = stmt.where(Reading.created_at <= to_date)
        stmt = stmt.order_by(Reading.created_at).offset(offset).limit(limit)

        readings = self.db.scalars(stmt).all()
        return [self._to_model(r) for r in readings]

    def get(self, reading_id: int) -> ReadingModel | None:
        reading = self.db.get(Reading, reading_id)
        return self._to_model(reading) if reading else None

    def update(
        self, reading_id: int, value: float | None = None, unit: str | None = None
    ) -> ReadingModel | None:
        reading = self.db.get(Reading, reading_id)
        if not reading:
            return None
        if value is not None:
            reading.value = value
        if unit is not None:
            reading.unit = unit
        self.db.commit()
        self.db.refresh(reading)
        return self._to_model(reading)

    def delete(self, reading_id: int) -> bool:
        reading = self.db.get(Reading, reading_id)
        if not reading:
            return False
        self.db.delete(reading)
        self.db.commit()
        return True

    @staticmethod
    def _to_model(r: Reading) -> ReadingModel:
        return ReadingModel(
            id=int(r.id),
            sensor_id=str(r.sensor_id),
            value=float(r.value),
            unit=str(r.unit),
        )