from typing import Any

from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor_schema import SensorCreate


class SensorService:
    def __init__(self, repo: SensorRepository) -> None:
        self.repo = repo

    def get_all(self, skip: int = 0, limit: int = 100) -> Any:
        return self.repo.get_all(skip=skip, limit=limit)

    def get_by_id(self, sensor_id: int) -> Any:
        sensor = self.repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        return sensor

    def create(self, sensor_data: SensorCreate) -> Any:
        return self.repo.add(
            name=sensor_data.name,
            type_=sensor_data.type,
            location=sensor_data.location,
            alert_threshold=sensor_data.alert_threshold,
        )

    def deactivate(self, sensor_id: int) -> bool:
        success = self.repo.deactivate(sensor_id)
        if not success:
            raise ValueError("Sensor no encontrado")
        return success