from app.repositories.alert_repo import AlertModel, AlertRepository
from app.repositories.reading_repo import ReadingModel
from app.services.alert_strategies import AlertStrategy
from app.services.anomaly import AnomalyService


class AlertService:
    """Evalua una lectura contra su umbral; si es anomala, la registra
    y notifica via la estrategia inyectada (OCP: nuevas formas de
    notificar no tocan esta clase)."""

    def __init__(
        self, repo: AlertRepository, strategy: AlertStrategy
    ) -> None:
        self._repo = repo
        self._strategy = strategy

    def evaluate(self, reading: ReadingModel) -> AlertModel | None:
        threshold = reading.alert_threshold
        if threshold is None:
            return None
        if not AnomalyService.is_anomalous(reading.value, threshold):
            return None

        message = (
            f"Sensor {reading.sensor_id}: lectura {reading.value} "
            f"supera el umbral {threshold}"
        )
        self._strategy.notify(message)

        return self._repo.add(
            sensor_id=int(reading.sensor_id),
            reading_id=reading.id,
            value=reading.value,
            threshold=threshold,
            message=message,
        )