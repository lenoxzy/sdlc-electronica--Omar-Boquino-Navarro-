from typing import Protocol, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import SensorModel  

# 1. El Protocolo: La interfaz que dicta las reglas (DIP)
class SensorRepository(Protocol):
    def add(self, name: str, type_: str, location: str) -> SensorModel: ...
    def get_all(self) -> Sequence[SensorModel]: ...
    def get_by_id(self, sensor_id: int) -> SensorModel | None: ...

# 2. La Implementación: La clase que realmente toca la base de datos
class SQLAlchemySensorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, name: str, type_: str, location: str) -> SensorModel:
        sensor = SensorModel(name=name, type=type_, location=location)
        self.db.add(sensor)
        self.db.commit()
        self.db.refresh(sensor)
        return sensor

    def get_all(self) -> Sequence[SensorModel]:
        # FIX: Sintaxis SQLAlchemy 2.x usando select() y scalars()
        stmt = select(SensorModel)
        return self.db.scalars(stmt).all()

    def get_by_id(self, sensor_id: int) -> SensorModel | None:
        # FIX: Sintaxis moderna para obtener por ID
        return self.db.get(SensorModel, sensor_id)