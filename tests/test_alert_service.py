from datetime import datetime

from app.repositories.alert_repo import AlertModel
from app.repositories.reading_repo import ReadingModel
from app.services.alert_service import AlertService
from app.services.alert_strategies import AlertStrategy


class FakeAlertRepository:
    def __init__(self) -> None:
        self.alerts: list[AlertModel] = []
        self._next_id = 1

    def add(
        self,
        sensor_id: int,
        reading_id: int,
        value: float,
        threshold: float,
        message: str,
    ) -> AlertModel:
        alert = AlertModel(
            id=self._next_id,
            sensor_id=sensor_id,
            reading_id=reading_id,
            value=value,
            threshold=threshold,
            message=message,
            created_at=datetime.now(),
        )
        self.alerts.append(alert)
        self._next_id += 1
        return alert

    def list_for_sensor(self, sensor_id: int) -> list[AlertModel]:
        return [a for a in self.alerts if a.sensor_id == sensor_id]

    def list_all(self, limit: int = 50, offset: int = 0) -> list[AlertModel]:
        return self.alerts


class FakeAlertStrategy(AlertStrategy):
    def __init__(self) -> None:
        self.messages: list[str] = []

    def notify(self, message: str) -> None:
        self.messages.append(message)


def _reading(value: float, threshold: float | None) -> ReadingModel:
    return ReadingModel(
        id=1, sensor_id="1", value=value, unit="C", alert_threshold=threshold
    )


def test_evaluate_creates_alert_when_value_exceeds_threshold() -> None:
    repo = FakeAlertRepository()
    strategy = FakeAlertStrategy()
    service = AlertService(repo=repo, strategy=strategy)

    result = service.evaluate(_reading(value=45.0, threshold=40.0))

    assert result is not None
    assert len(repo.alerts) == 1
    assert len(strategy.messages) == 1


def test_evaluate_returns_none_when_value_within_threshold() -> None:
    repo = FakeAlertRepository()
    strategy = FakeAlertStrategy()
    service = AlertService(repo=repo, strategy=strategy)

    result = service.evaluate(_reading(value=20.0, threshold=40.0))

    assert result is None
    assert len(repo.alerts) == 0


def test_evaluate_skips_check_when_sensor_has_no_threshold() -> None:
    repo = FakeAlertRepository()
    strategy = FakeAlertStrategy()
    service = AlertService(repo=repo, strategy=strategy)

    result = service.evaluate(_reading(value=999.0, threshold=None))

    assert result is None
    assert len(repo.alerts) == 0


def test_evaluate_is_ocp_swappable_with_new_strategy() -> None:
    """Nueva estrategia sin tocar AlertService: evidencia concreta de OCP."""

    class SpyStrategy(AlertStrategy):
        def __init__(self) -> None:
            self.called_with: str | None = None

        def notify(self, message: str) -> None:
            self.called_with = message

    repo = FakeAlertRepository()
    spy = SpyStrategy()
    service = AlertService(repo=repo, strategy=spy)

    service.evaluate(_reading(value=100.0, threshold=50.0))

    assert spy.called_with is not None