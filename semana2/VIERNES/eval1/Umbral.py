from typing import Protocol

from US_01 import (
    SensorReading,  # Asegúrate de que tu archivo se llame us_01.py en minúsculas
)


# Definimos el contrato de la alerta (Inversión de Dependencias)
class AlertStrategy(Protocol):
    def send_alert(self, message: str) -> None: ...


class AnomalyDetector:
    def __init__(
        self, alert_strategy: AlertStrategy, temp_threshold: float, hum_threshold: float
    ):
        self._alert = alert_strategy
        self._temp_threshold = temp_threshold
        self._hum_threshold = hum_threshold

    def check(self, reading: SensorReading) -> None:
        if (
            reading.reading_type == "temperature"
            and reading.value > self._temp_threshold
        ):
            self._alert.send_alert(
                f"CRITICAL TEMP: {reading.value}°C from {reading.sensor_id}"
            )

        elif reading.reading_type == "humidity" and reading.value > self._hum_threshold:
            self._alert.send_alert(
                f"CRITICAL HUM: {reading.value}% from {reading.sensor_id}"
            )
