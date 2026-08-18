import logging

from app.repositories.reading_repo import ReadingModel

logger = logging.getLogger(__name__)


class AnomalyService:
    """Servicio para detectar y registrar anomalías en lecturas de sensores."""

    def __init__(self, logger_instance: logging.Logger | None = None) -> None:
        self._logger = logger_instance or logger

    @staticmethod
    def is_anomalous(value: float, threshold: float) -> bool:
        """Determina si una lectura supera el umbral de alerta configurado."""
        return value > threshold

    def check(self, reading: ReadingModel, threshold: float) -> bool:
        """Verifica si la lectura es anómala y registra el resultado."""
        anomalous = self.is_anomalous(reading.value, threshold)

        if anomalous:
            self._logger.warning(
                "Anomalía detectada en lectura (valor: %s, umbral: %s)",
                reading.value,
                threshold,
            )
        else:
            self._logger.info(
                "Lectura normal (valor: %s, umbral: %s)", reading.value, threshold
            )

        return anomalous
