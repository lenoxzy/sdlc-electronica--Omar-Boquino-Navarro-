# S - Una clase, una responsabilidad: SensorReader lee; DataLogger persiste.
# O - AlertStrategy (ABC) con ConsoleAlert y FileAlert: agregar EmailAlert
#     manana NO toca el codigo existente.
# L - TemperatureSensor y HumiditySensor son intercambiables donde se espera
#     BaseSensor: process_sensor(sensor: BaseSensor) funciona con cualquiera.
 
class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...
 
class AnomalyDetector:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold
 
    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalia en {reading.sensor_id}")
