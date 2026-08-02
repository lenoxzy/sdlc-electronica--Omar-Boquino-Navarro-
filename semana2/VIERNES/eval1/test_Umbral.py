from Umbral import AnomalyDetector
from US_01 import SensorReading


# 1. Creamos un "Mock" (Simulador)
class MockAlert:
    def __init__(self):
        self.messages = []

    def send_alert(self, message: str) -> None:
        self.messages.append(message)


# Test 1: Entra al 'if' de Temperatura
def test_detector_temperatura_critica():
    mock = MockAlert()
    detector = AnomalyDetector(mock, temp_threshold=35.0, hum_threshold=80.0)
    lectura = SensorReading("T1", 40.0, "temperature")

    detector.check(lectura)
    assert len(mock.messages) == 1
    assert "CRITICAL TEMP" in mock.messages[0]


# Test 2: Entra al 'elif' de Humedad
def test_detector_humedad_critica():
    mock = MockAlert()
    detector = AnomalyDetector(mock, temp_threshold=35.0, hum_threshold=80.0)
    lectura = SensorReading("H1", 85.0, "humidity")

    detector.check(lectura)
    assert len(mock.messages) == 1
    assert "CRITICAL HUM" in mock.messages[0]


# Test 3: No entra a ninguno (Valores normales)
def test_detector_valores_normales():
    mock = MockAlert()
    detector = AnomalyDetector(mock, temp_threshold=35.0, hum_threshold=80.0)
    lectura = SensorReading("T1", 20.0, "temperature")

    detector.check(lectura)
    assert len(mock.messages) == 0  # La lista debe estar vacía porque no hubo alerta
