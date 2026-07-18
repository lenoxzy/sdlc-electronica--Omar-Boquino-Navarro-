import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(__file__))

from sensor_system import (
    SensorReading, SensorReader, DataLogger,
    ConsoleAlert, EmailAlert, AnomalyDetector,
    TemperatureSensor, HumiditySensor, process_sensor
)

# ==========================================
# Pruebas para SRP (Responsabilidad Única)
# ==========================================
def test_sensor_reader():
    """Prueba que el lector devuelva correctamente la estructura de datos."""
    reader = SensorReader()
    lectura = reader.read_data("TEST-01")
    
    assert lectura.sensor_id == "TEST-01"
    assert lectura.value == 25.5
    assert isinstance(lectura, SensorReading)

def test_data_logger(capsys):
    """Prueba que el logger formatee e imprima bien el mensaje de guardado."""
    logger = DataLogger()
    lectura = SensorReading("TEST-02", 15.0)
    
    logger.save(lectura)
    # capsys captura lo que el programa intentó imprimir en consola
    captured = capsys.readouterr() 
    
    assert "Guardando lectura de TEST-02: 15.0 en la base de datos." in captured.out

# ==========================================
# Pruebas para OCP (Abierto/Cerrado)
# ==========================================
def test_anomaly_detector_triggers_alert(capsys):
    """Prueba que la anomalía se detecte y dispare la alerta correspondiente si supera el umbral."""
    # Umbral de 20.0, enviamos 25.5 (Debe alertar)
    detector = AnomalyDetector(ConsoleAlert(), threshold=20.0)
    lectura = SensorReading("TEMP-ALERT", 25.5)
    
    detector.check(lectura)
    captured = capsys.readouterr()
    
    assert "[ALERTA CONSOLA]: Anomalía detectada en TEMP-ALERT. Valor: 25.5" in captured.out

def test_anomaly_detector_no_alert(capsys):
    """Prueba que NO se dispare ninguna alerta si el valor es menor o igual al umbral."""
    # Umbral de 30.0, enviamos 25.5 (NO debe alertar)
    detector = AnomalyDetector(EmailAlert(), threshold=30.0)
    lectura = SensorReading("TEMP-SAFE", 25.5)
    
    detector.check(lectura)
    captured = capsys.readouterr()
    
    # La consola debe estar vacía porque no se cumplió la condición del if
    assert captured.out == "" 

# ==========================================
# Pruebas para LSP (Sustitución de Liskov)
# ==========================================
def test_temperature_and_humidity_sensors():
    """Prueba que los sensores hijos midan correctamente sus valores por defecto."""
    temp = TemperatureSensor("T1")
    hum = HumiditySensor("H1")
    
    assert temp.measure() == 22.5
    assert hum.measure() == 60.0

def test_process_sensor_liskov(capsys):
    """
    Prueba que la función process_sensor acepte sin problemas a los hijos 
    de BaseSensor y los procese correctamente (Cumpliendo LSP).
    """
    temp_sensor = TemperatureSensor("TEMP-ZN1")
    process_sensor(temp_sensor)
    
    captured = capsys.readouterr()
    assert "Procesando sensor TEMP-ZN1. Medición actual: 22.5" in captured.out
    
    hum_sensor = HumiditySensor("HUM-ZN1")
    process_sensor(hum_sensor)
    
    captured_hum = capsys.readouterr()
    assert "Procesando sensor HUM-ZN1. Medición actual: 60.0" in captured_hum.out
