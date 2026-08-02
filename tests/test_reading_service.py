import pytest

from app.repositories.reading_repo import ReadingModel
from app.services.reading_service import ReadingService


# 1. El Repositorio Fake (en memoria)
class FakeReadingRepository:
    def __init__(self):
        self.readings: list[ReadingModel] = []
        self._current_id = 1

    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        reading = ReadingModel(
            id=self._current_id, sensor_id=sensor_id, value=value, unit=unit
        )
        self.readings.append(reading)
        self._current_id += 1
        return reading

    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return [r for r in self.readings if r.sensor_id == sensor_id]


# 2. Los Tests
def test_record_successful():
    """Prueba que una lectura válida se guarda correctamente a través del servicio."""
    # Arrange (Preparar)
    fake_repo = FakeReadingRepository()
    service = ReadingService(repo=fake_repo)

    # Act (Actuar)
    result = service.record(sensor_id="TEMP-01", value=25.0, unit="C")

    # Assert (Afirmar)
    assert result.value == 25.0
    assert result.sensor_id == "TEMP-01"
    assert len(fake_repo.readings) == 1


def test_record_fails_below_absolute_zero():
    """no se permiten temperaturas menores al cero absoluto."""
    # Arrange
    fake_repo = FakeReadingRepository()
    service = ReadingService(repo=fake_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Temperatura por debajo del cero absoluto"):
        service.record(sensor_id="TEMP-01", value=-274.0, unit="C")

    # Verificamos que el repositorio falso quedó vacío 
    assert len(fake_repo.readings) == 0
