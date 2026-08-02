from sqlalchemy.orm import Session

from app.models.models import Sensor
from app.schemas.sensor_schema import SensorCreate


class SQLAlchemySensorRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_sensors(self) -> list[Sensor]:
        return self.db.query(Sensor).all()

    def get_sensor(self, sensor_id: int) -> Sensor | None:
        return self.db.query(Sensor).filter(Sensor.id == sensor_id).first()

    def add(self, sensor_data: SensorCreate) -> Sensor:
        new_sensor = Sensor(
            name=sensor_data.name,
            type=sensor_data.type,
            location=sensor_data.location
        )
        self.db.add(new_sensor)
        self.db.commit()
        self.db.refresh(new_sensor)
        return new_sensor

    def delete(self, sensor_id: int) -> bool:
        sensor = self.get_sensor(sensor_id)
        if sensor:
            self.db.delete(sensor)
            self.db.commit()
            return True
        return False