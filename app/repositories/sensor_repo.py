from collections.abc import Sequence
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Sensor


class SensorRepository(Protocol):
    def add(
        self,
        name: str,
        type_: str,
        location: str | None = None,
        alert_threshold: float | None = None,
    ) -> Sensor: ...
    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Sensor]: ...
    def get_by_id(self, sensor_id: int) -> Sensor | None: ...
    def deactivate(self, sensor_id: int) -> bool: ...


class SQLAlchemySensorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(
        self,
        name: str,
        type_: str,
        location: str | None = None,
        alert_threshold: float | None = None,
    ) -> Sensor:
        sensor = Sensor(
            name=name,
            type=type_,
            location=location,
            alert_threshold=alert_threshold,
        )
        self.db.add(sensor)
        self.db.commit()
        self.db.refresh(sensor)
        return sensor

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Sensor]:
        stmt = (
            select(Sensor)
            .where(Sensor.is_active.is_(True))
            .offset(skip)
            .limit(limit)
        )
        return self.db.scalars(stmt).all()

    def get_by_id(self, sensor_id: int) -> Sensor | None:
        return self.db.get(Sensor, sensor_id)

    def deactivate(self, sensor_id: int) -> bool:
        sensor = self.db.get(Sensor, sensor_id)
        if not sensor:
            return False
        sensor.is_active = False
        self.db.commit()
        return True