from typing import Any  
from app.repositories.sensor_repo import SQLAlchemySensorRepository
from app.schemas.sensor_schema import SensorCreate


class SensorService:
    def __init__(self, repo: SQLAlchemySensorRepository) -> None: 
        self.repo = repo

    def get_all(self, skip: int = 0, limit: int = 100) -> Any: 
        return self.repo.list_sensors(skip=skip, limit=limit)

    def get_by_id(self, sensor_id: int) -> Any: 
        sensor = self.repo.get_sensor(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        return sensor

    def create(self, sensor_data: SensorCreate) -> Any: 
        return self.repo.add(sensor_data)

    def delete(self, sensor_id: int) -> bool: 
        success = self.repo.delete(sensor_id)
        if not success:
            raise ValueError("Sensor no encontrado")
        return success