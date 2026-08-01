
from __future__ import annotations

from dataclasses import dataclass


# --- US-01: Modelo Inmutable ---
@dataclass(frozen=True)
class SensorReading:
    """Almacena la lectura del hardware de forma inmutable."""
    sensor_id: str
    value: float
    reading_type: str  # 'temperature' o 'humidity'