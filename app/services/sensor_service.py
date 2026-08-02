from app.repositories.sensor_repo import SQLAlchemySensorRepository
from app.schemas.sensor_schema import SensorCreate


class SensorService:
    def __init__(self, repo: SQLAlchemySensorRepository):
        self.repo = repo

    def get_all(self):
        return self.repo.list_sensors()

    def get_by_id(self, sensor_id: int):
        sensor = self.repo.get_sensor(sensor_id)
        if not sensor:
            raise ValueError("Sensor no encontrado")
        return sensor

    def create(self, sensor_data: SensorCreate):
        return self.repo.add(sensor_data)

    def delete(self, sensor_id: int):
        success = self.repo.delete(sensor_id)
        if not success:
            raise ValueError("Sensor no encontrado")
        return success