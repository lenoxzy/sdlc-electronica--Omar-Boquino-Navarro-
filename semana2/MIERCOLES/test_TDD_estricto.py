import pytest
from ingestion import process_sensor_data 

def test_ingesta_sin_temperatura_lanza_error():
    payload_invalido = {
        "sensor_id": "DHT11_01",
        "humedad": 55.0
        # Falta "temperatura"
    }

    # Act & Assert (Actuar y Afirmar)
    # Verificamos que al intentar procesarlo, el sistema levante un ValueError
    with pytest.raises(ValueError, match="El campo temperatura es obligatorio"):
        process_sensor_data(payload_invalido)
