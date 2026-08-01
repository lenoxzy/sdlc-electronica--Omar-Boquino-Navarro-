from typing import Protocol
from dataclasses import dataclass

@dataclass
class ReadingModel:
    id: int
    sensor_id: str
    value: float
    unit: str

class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]: ...