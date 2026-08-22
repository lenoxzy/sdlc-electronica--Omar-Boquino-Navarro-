from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.alert_status import validate_status_transition
from app.models.models import Alert


@dataclass
class AlertModel:
    id: int
    sensor_id: int
    reading_id: int
    value: float
    threshold: float
    message: str
    status: str
    created_at: datetime


class AlertRepository(Protocol):
    def add(
        self,
        sensor_id: int,
        reading_id: int,
        value: float,
        threshold: float,
        message: str,
    ) -> AlertModel: ...
    def list_for_sensor(self, sensor_id: int) -> list[AlertModel]: ...
    def list_all(self, limit: int = 50, offset: int = 0) -> list[AlertModel]: ...
    def get(self, alert_id: int) -> AlertModel | None: ...
    def update_status(self, alert_id: int, status: str) -> AlertModel | None: ...


class SQLAlchemyAlertRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(
        self,
        sensor_id: int,
        reading_id: int,
        value: float,
        threshold: float,
        message: str,
    ) -> AlertModel:
        alert = Alert(
            sensor_id=sensor_id,
            reading_id=reading_id,
            value=value,
            threshold=threshold,
            message=message,
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return self._to_model(alert)

    def list_for_sensor(self, sensor_id: int) -> list[AlertModel]:
        stmt = (
            select(Alert)
            .where(Alert.sensor_id == sensor_id)
            .order_by(Alert.created_at.desc())
        )
        alerts = self.db.scalars(stmt).all()
        return [self._to_model(a) for a in alerts]

    def list_all(self, limit: int = 50, offset: int = 0) -> list[AlertModel]:
        stmt = (
            select(Alert)
            .order_by(Alert.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        alerts = self.db.scalars(stmt).all()
        return [self._to_model(a) for a in alerts]

    def get(self, alert_id: int) -> AlertModel | None:
        alert = self.db.get(Alert, alert_id)
        return self._to_model(alert) if alert else None

    def update_status(self, alert_id: int, status: str) -> AlertModel | None:
        validate_status_transition(status)  # lanza ValueError si es invalido
        alert = self.db.get(Alert, alert_id)
        if not alert:
            return None
        alert.status = status
        self.db.commit()
        self.db.refresh(alert)
        return self._to_model(alert)

    @staticmethod
    def _to_model(a: Alert) -> AlertModel:
        return AlertModel(
            id=int(a.id),
            sensor_id=int(a.sensor_id),
            reading_id=int(a.reading_id),
            value=float(a.value),
            threshold=float(a.threshold),
            message=str(a.message),
            status=str(a.status),
            created_at=a.created_at,
        )