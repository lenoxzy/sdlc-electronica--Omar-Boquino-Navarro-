import pytest
from registry import SensorRegistry, SensorNotFoundError


def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")