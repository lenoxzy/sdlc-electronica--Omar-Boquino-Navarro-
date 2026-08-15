import logging
from typing import Any

logger = logging.getLogger(__name__)


class AnomalyService:
    """Servicio para detectar y registrar anomalías en lecturas de sensores."""

    def __init__(self, logger_instance: logging.Logger | None = None) -> None:
        self._logger = logger_instance or logger

    @staticmethod
    def is_anomalous(value: float, threshold: float) -> bool:
        """Determina si un valor numérico supera el umbral establecido."""
        return abs(value) > threshold

    def check(self, reading: Any, threshold: float) -> bool:
        """
        Verifica si la lectura es anomalía y registra el resultado.

        Soporta lecturas con atributo 'value' u objetos dict/similares.
        """
        value = reading.value if hasattr(reading, "value") else reading["value"]
        anomalous = self.is_anomalous(value, threshold)

        if anomalous:
            self._logger.warning(
                "Anomalía detectada en lectura (valor: %s, umbral: %s)",
                value,
                threshold,
            )
        else:
            self._logger.info(
                "Lectura normal (valor: %s, umbral: %s)",
                value,
                threshold,
            )

        return anomalous
