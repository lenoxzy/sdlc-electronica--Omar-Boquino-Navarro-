from simulator import SensorSimulator
from Umbral import (
    AnomalyDetector,  # Ajusta si tu archivo de umbrales se llama diferente
)


class IntegrationAlertMock:
    """Mock especializado para contar la ráfaga de alertas del test de integración"""
    def __init__(self):
        self.alerts_sent = 0
        
    def send_alert(self, message: str) -> None:
        self.alerts_sent += 1

def test_simulacion_bodega_completa():
    # 1. Preparar el entorno (Arrange)
    # Forzamos la semilla para que los "aleatorios" sean los mismos siempre
    simulator = SensorSimulator(seed=42) 
    alert_system = IntegrationAlertMock()
    detector = AnomalyDetector(alert_system, temp_threshold=35.0, hum_threshold=80.0)
    # set de sensores y ciclos

    sensores = [f"SENSOR-{i:02d}" for i in range(1, 11)] # SENSOR-01 a SENSOR-10
    ciclos = 60
    alertas_esperadas = 0

    # 2. Ejecutar la simulación masiva (Act)
    for _ in range(ciclos):
        for sensor_id in sensores:
            # Simulamos e inyectamos Temperatura
            t_read = simulator.read_sensor(sensor_id, "temperature")
            if t_read.value > 35.0:
                alertas_esperadas += 1
            detector.check(t_read)
            
            # Simulamos e inyectamos Humedad
            h_read = simulator.read_sensor(sensor_id, "humidity")
            if h_read.value > 80.0:
                alertas_esperadas += 1
            detector.check(h_read)

    # 3. Verificar resultados (Assert)
    # Verificamos que el sistema procesó 1200 lecturas y detectó EXACTAMENTE 
    assert alert_system.alerts_sent == alertas_esperadas
    assert alert_system.alerts_sent > 0, "Debería haberse generado al menos 1 alerta"