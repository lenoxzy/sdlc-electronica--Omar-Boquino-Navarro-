import pytest
from US_01 import SensorReading

# Test US-01: Ingesta de datos
def test_sensor_reading_creation():
    reading = SensorReading(sensor_id="TEMP-01", value=36.5, reading_type="temperature")
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 36.5
    assert reading.reading_type == "temperature"