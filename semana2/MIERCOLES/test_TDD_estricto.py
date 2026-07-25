#importamos librerias 
import pytest
from registry import SensorRegistry, SensorNotFoundError
#se deja igual al codigo original 
def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")
