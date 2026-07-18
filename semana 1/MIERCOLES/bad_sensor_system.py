from dataclasses import dataclass
from abc import ABC, abstractmethod
@dataclass
class SensorReading:
    sensor_id: str
    value: float
#Etapa sin  SINGLE RESPONSIBILITY   
class SensorReader:
    def read_data(self, sensor_id: str) -> SensorReading:
        # Simulamos la lectura de un sensor 
        print(f"sensor {sensor_id}...")
        return SensorReading(sensor_id=sensor_id, value=30)# Uso:
    def save(self, reading: SensorReading) -> None:
        # Simulamos guardar en una base de datos o archivo
        print(f"Guardando lectura de {reading.sensor_id}: {reading.value} en la base de datos.")


#Etapa sin OPEN/CLOSED
class AnomalyDetector:
    # Recibimos un simple string ('consola', 'archivo', 'email') en lugar de una interfaz
    def __init__(self, alert_type: str, threshold: float) -> None:
        self._alert_type = alert_type
        self._threshold = threshold

    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            mensaje = f"Anomalía detectada en {reading.sensor_id}. Valor: {reading.value}"
            # Si queremos agregar 'sms', tenemos que modificar este bloque de código.
            if self._alert_type == "consola":
                print(f"[ALERTA CONSOLA]: {mensaje}")
            
            elif self._alert_type == "archivo":
                print(f"[ALERTA ARCHIVO]: Escribiendo '{mensaje}' en alerts.log")
            
            elif self._alert_type == "email":
                print(f"[ALERTA EMAIL]: Enviando correo -> {mensaje}")
            
            else:
                print("Tipo de alerta no soportado.")
                
   #Etapa sin LISKOV           

class BaseSensor(ABC):
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id

    @abstractmethod
    def measure(self):
        # Se espera que devuelva un valor numérico (float o int)
        pass

class TemperatureSensor(BaseSensor):
    def measure(self):
        return 25.5  # Comportamiento correcto, devuelve un número

class HumiditySensor(BaseSensor):
    def measure(self):
        return 60.0  # Comportamiento correcto, devuelve un número
class DoorSensor(BaseSensor):
    def measure(self):
        # Una puerta no tiene un valor numérico, está abierta o cerrada.
        return "ABIERTA" 

# --- Código Cliente ---
def analizar_medicion(sensor: BaseSensor, threshold: float) -> None:
    print(f"Analizando sensor {sensor.sensor_id}...")
    valor = sensor.measure()
    
    # El sistema asume que 'valor' es un número porque TODOS los BaseSensor  deberían comportarse igual.
    if valor > threshold:
        print(f"¡Alerta! El valor {valor} superó el umbral de {threshold}")
    else:
        print("Todo normal.")

# Uso correcto:
sensor_temp = TemperatureSensor("TEMP-01")
analizar_medicion(sensor_temp, 20.0) 
# Imprime: ¡Alerta! El valor 25.5 superó el umbral... (Todo bien)

# Uso INcorrecto (Falla por violar LSP):
sensor_puerta = DoorSensor("DOOR-01")
from abc import ABC, abstractmethod

class BaseSensor(ABC):
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id

    @abstractmethod
    def measure(self):
        # Se espera que devuelva un valor numérico (float o int)
        pass

class TemperatureSensor(BaseSensor):
    def measure(self):
        return 25.5  # Comportamiento correcto, devuelve un número

class HumiditySensor(BaseSensor):
    def measure(self):
        return 60.0  # Comportamiento correcto, devuelve un número

# violacion a LPS
# Hereda de BaseSensor, pero cambia el tipo de respuesta a un string.
class DoorSensor(BaseSensor):
    def measure(self):
        # Una puerta no tiene un valor numérico, está abierta o cerrada.
        return "ABIERTA" 

# --- Código Cliente ---
def analizar_medicion(sensor: BaseSensor, threshold: float) -> None:
    print(f"Analizando sensor {sensor.sensor_id}...")
    valor = sensor.measure()
    
    # El sistema asume que 'valor' es un número porque TODOS los BaseSensor 
    # deberían comportarse igual.
    if valor > threshold:
        print(f"¡Alerta! El valor {valor} superó el umbral de {threshold}")
    else:
        print("Todo normal.")
        







# Uso:
reader = SensorReader()
logger = SensorReader()
lectura = reader.read_data("DHT11")
logger.save(lectura)
# Uso:
detector_consola = AnomalyDetector("consola", threshold=20.0)
detector_consola.check(SensorReading("TEMP-01", 25.5))

detector_email = AnomalyDetector("email", threshold=20.0)
detector_email.check(SensorReading("TEMP-02", 30.0))

# Uso correcto:
sensor_temp = TemperatureSensor("TEMP-01")
analizar_medicion(sensor_temp, 20.0) 
