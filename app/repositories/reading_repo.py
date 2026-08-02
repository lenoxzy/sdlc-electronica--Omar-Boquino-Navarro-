from dataclasses import dataclass
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
    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]: ...


# --- 3. LA IMPLEMENTACIÓN REAL (Capa de Datos) ---
class SQLAlchemyReadingRepository:
    """Implementación real del repositorio usando SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        # Buscamos si existe el sensor
        sensor = self.db.get(Sensor, int(sensor_id))
        if not sensor:
            raise ValueError("Sensor no encontrado")

        # Creamos la lectura
        new_reading = Reading(value=value, unit=unit, sensor_id=sensor.id)
        self.db.add(new_reading)
        self.db.commit()
        self.db.refresh(new_reading)

        return ReadingModel(
            id=new_reading.id,
            sensor_id=str(new_reading.sensor_id),
            value=new_reading.value,
            unit=new_reading.unit,
        )

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        stmt = select(Reading).where(Reading.sensor_id == int(sensor_id))
        readings = self.db.scalars(stmt).all()
        return [
            ReadingModel(
                id=r.id, sensor_id=str(r.sensor_id), value=r.value, unit=r.unit
            )
            for r in readings
        ]
