from typing import Protocol
from dataclasses import dataclass
# 1. Definimos el modelo de datos básico
@dataclass
class SensorReading:
    sensor_id: str
    value: float
# 2. El Protocolo
class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...
# 3. El Procesador que inyecta la dependencia
class DataProcessor:
    """Depende de la abstraccion, no de una implementacion concreta."""
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # inyección de dependencias
        
    def process_and_save(self, reading: SensorReading) -> None:
        # Lógica de negocio iría aquí
        self._repo.save(reading)
class InMemoryRepository:
    """Simula una base de datos usando un diccionario."""
    def __init__(self) -> None:
        self._data: dict[str, SensorReading] = {}

    def save(self, reading: SensorReading) -> None:
        self._data[reading.sensor_id] = reading

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self._data.get(sensor_id)
