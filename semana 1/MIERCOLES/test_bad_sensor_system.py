import pytest
from bad_sensor_system import (
    SensorReading, 
    SensorReader, 
    AnomalyDetector, 
    TemperatureSensor, 
    DoorSensor, 
    analizar_medicion
)

# ==========================================
# Pruebas para violación SRP (Responsabilidad Única)
# ==========================================
def test_sensor_reader_hace_demasiado(capsys):
    """
    Prueba que SensorReader viola SRP al encargarse tanto de leer 
    como de guardar en la base de datos.
    """
    reader = SensorReader()
    
    # Probamos su primera responsabilidad (Leer)
    lectura = reader.read_data("TEST-01")
    assert lectura.value == 30
    
    # Probamos su segunda responsabilidad (Guardar)
    reader.save(lectura)
    captured = capsys.readouterr()
    
    assert "Guardando lectura de TEST-01: 30" in captured.out

# ==========================================
# Pruebas para violación OCP (Abierto/Cerrado)
# ==========================================
def test_anomaly_detector_hardcoded_alerts(capsys):
    """
    Prueba que AnomalyDetector usa condicionales rígidos (if/elif)
    y funciona para los casos programados.
    """
    detector = AnomalyDetector("consola", threshold=20.0)
    detector.check(SensorReading("T1", 25.0))
    
    captured = capsys.readouterr()
    assert "[ALERTA CONSOLA]: Anomalía detectada" in captured.out

def test_anomaly_detector_no_soportado(capsys):
    """
    Prueba la limitación del OCP: Si le pasamos un tipo de alerta 
    nuevo ('sms') que no está en sus 'if/elif', el sistema falla silenciosamente.
    """
    detector_nuevo = AnomalyDetector("sms", threshold=20.0)
    detector_nuevo.check(SensorReading("T2", 30.0))
    
    captured = capsys.readouterr()
    # Verifica que el código caiga en el 'else' por no estar preparado para la extensión
    assert "Tipo de alerta no soportado." in captured.out

# ==========================================
# Pruebas para violación LSP (Sustitución de Liskov)
# ==========================================
def test_liskov_uso_correcto(capsys):
    """
    Prueba que el código cliente funciona con la clase hija esperada.
    """
    sensor_temp = TemperatureSensor("TEMP-OK")
    analizar_medicion(sensor_temp, 20.0)
    
    captured = capsys.readouterr()
    assert "¡Alerta! El valor 25.5 superó el umbral de 20.0" in captured.out

def test_liskov_violacion_rompe_el_programa():
    """
    Prueba que al pasar una clase hija que viola Liskov (DoorSensor devuelve un str),
    el programa cliente colapsa con un TypeError al intentar hacer: "ABIERTA" > threshold.
    """
    sensor_puerta = DoorSensor("DOOR-BAD")
    
    # Le decimos a pytest: "Ejecuta esto, sé que va a explotar con un TypeError, 
    # y si explota como espero, la prueba pasa".
    with pytest.raises(TypeError) as error_info:
        analizar_medicion(sensor_puerta, 20.0)
    
    # Opcional: Podemos validar que el error fue por intentar comparar str con float
    assert "not supported between instances of 'str' and 'float'" in str(error_info.value)
