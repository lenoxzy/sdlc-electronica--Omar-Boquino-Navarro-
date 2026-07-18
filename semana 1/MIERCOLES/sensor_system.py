from dataclasses import dataclass
from abc import ABC, abstractmethod
@dataclass
class SensorReading:
    sensor_id: str
    value: float

# - Principio de Responsabilidad Única (SRP)
class SensorReader:
    """Responsabilidad: Únicamente leer datos del sensor."""
    def read_data(self, sensor_id: str) -> SensorReading:
        # Simulamos la lectura de un sensor físico
        print(f"Leyendo datos del sensor {sensor_id}...")
        return SensorReading(sensor_id=sensor_id, value=25.5)

class DataLogger:
    """Responsabilidad: Únicamente persistir (guardar) los datos."""
    def save(self, reading: SensorReading) -> None:
        # Simulamos guardar en una base de datos o archivo
        print(f"Guardando lectura de {reading.sensor_id}: {reading.value} en la base de datos.")


#- Principio de Abierto/Cerrado (OCP)



class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None: 
        pass

# Implementaciones originales
class ConsoleAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"[ALERTA CONSOLA]: {message}")

class FileAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"[ALERTA ARCHIVO]: Escribiendo '{message}' en alerts.log")

# Extensión: Agregamos EmailAlert SIN modificar las clases de arriba ni la clase que las use.
class EmailAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"[ALERTA EMAIL]: Enviando correo -> {message}")

class AnomalyDetector:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold

    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalía detectada en {reading.sensor_id}. Valor: {reading.value}")


#- Principio de Sustitución de Liskov (LSP)


class BaseSensor(ABC):
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id

    @abstractmethod
    def measure(self) -> float:
        pass

class TemperatureSensor(BaseSensor):
    def measure(self) -> float:
        # Lógica específica para medir temperatura
        return 22.5

class HumiditySensor(BaseSensor):
    def measure(self) -> float:
        # Lógica específica para medir humedad
        return 60.0

# Esta función depende de la abstracción, no de las clases hijas.
def process_sensor(sensor: BaseSensor) -> None:
    # Funciona idénticamente con cualquier subclase
    valor = sensor.measure()
    print(f"Procesando sensor {sensor.sensor_id}. Medición actual: {valor}")

# Uso:
detector_consola = AnomalyDetector(ConsoleAlert(), threshold=20.0)
detector_consola.check(SensorReading("TEMP-01", 25.5))
# usamos EmailAlert sin modificar AnomalyDetector
detector_email = AnomalyDetector(EmailAlert(), threshold=20.0)
detector_email.check(SensorReading("TEMP-02", 30.0))

# Uso:
reader = SensorReader()
logger = DataLogger()
lectura = reader.read_data("TEMP-01")
logger.save(lectura)

# Uso:
sensor_temp = TemperatureSensor("TEMPEMPERATURA-SENSOR")
sensor_hum = HumiditySensor("HUMEDAD-SENSOR")
# Ambas subclases sustituyen a la clase base sin romper el programa
process_sensor(sensor_temp)
process_sensor(sensor_hum)
