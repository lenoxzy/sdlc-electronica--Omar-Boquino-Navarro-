from app.models.models import Sensor
from app.repositories.sensor_repo import SQLAlchemySensorRepository
from tests.conftest import TestingSessionLocal


def test_deactivate_sets_is_active_false_but_keeps_row() -> None:
    db = TestingSessionLocal()
    repo = SQLAlchemySensorRepository(db)
    sensor = repo.add(name="Soft Delete Test", type_="temperature")

    result = repo.deactivate(sensor.id)

    assert result is True
    refreshed = db.get(Sensor, sensor.id)
    assert refreshed is not None  # el registro SIGUE existiendo en la BD
    assert refreshed.is_active is False
    db.close()