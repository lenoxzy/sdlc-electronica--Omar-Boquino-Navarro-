from dataclasses import dataclass
import threading
from collections import deque
import json
import logging
from datetime import datetime, timezone
from typing import Protocol
@dataclass(frozen=True)
class SensorReading:
    """
    SRP: Su única responsabilidad es almacenar la lectura pura del sensor.
    Al ser frozen=True, garantizamos la inmutabilidad requerida en la prueba.
    """
    sensor_id: str
    value: float
    # Si la trama de tu sensor UART envía más datos (ej. timestamp, unidad),
    # se agregarían aquí.
################################################
# Asumimos que SensorReading está importado desde tu archivo de modelos
# from models import SensorReading 

# 1. El Contrato (ISP / DIP)
class DataParser(Protocol):
    """
    Define la regla estricta: todo parser debe tener un método 'parse' 
    que reciba un string y devuelva un SensorReading inmutable.
    """
    def parse(self, raw_data: str) -> SensorReading: ...

# 2. La Implementación Concreta (SRP y OCP)
class JSONUARTParser:
    """
    SRP: Su única responsabilidad es interpretar formato JSON.
    OCP: Si cambias a formato Hexadecimal, creas otra clase en lugar de modificar esta.
    """
    def parse(self, raw_data: str) -> SensorReading:
        try:
            # Asumimos que el UART manda algo como: '{"id": "A1", "val": 25.4}'
            data = json.loads(raw_data)
            return SensorReading(
                sensor_id=data.get("id", "UNKNOWN"),
                value=float(data.get("val", 0.0))
            )
        except json.JSONDecodeError:
            # Manejo básico si el cable metió ruido y el JSON llega roto
            raise ValueError("Trama UART corrupta o formato inválido")

######################anexo de la extension#####################################

#############1. Tercer Protocolo (CAN Simplificado)
class CANParser:
    """
    OCP en acción: Agregamos soporte para CAN bus sin modificar el driver.
    Asumimos un formato simplificado tipo: 'CAN_ID:SENS_03 VAL:45.2'
    """
    def parse(self, raw_data: str) -> SensorReading:
        try:
            # Lógica básica de separación de la trama CAN
            partes = raw_data.strip().split(" ")
            sensor_id = partes[0].split(":")[1]
            valor = float(partes[1].split(":")[1])
            return SensorReading(sensor_id=sensor_id, value=valor)
        except (IndexError, ValueError):
            raise ValueError("Trama CAN corrupta o formato inválido")

#####2. Buffer Circular Thread-Safe

class ThreadSafeCircularRecorder:
    """
    Buffer en RAM seguro para entornos multi-hilo.
    Mantiene solo las últimas 'max_size' lecturas.
    """
    def __init__(self, max_size: int = 100) -> None:
        # deque con maxlen actúa como un buffer circular nativo en Python
        self._buffer: deque[SensorReading] = deque(maxlen=max_size)
        # El candado (Lock) asegura la exclusión mutua
        self._lock = threading.Lock()

    def save(self, reading: SensorReading) -> None:
        # El bloque 'with' adquiere el candado y lo libera automáticamente
        with self._lock:
            self._buffer.append(reading)
            
    def get_all(self) -> list[SensorReading]:
        with self._lock:
            return list(self._buffer)

#####3. Logging Estructurado JSON 

# Configuramos el logger nativo de Python a nivel INFO
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("SensorHub")

class JSONLoggingRecorderWrapper:
    """
    Aplica el Patrón Decorator: Toma un grabador existente,
    emite un log estructurado en formato JSON y luego guarda el dato.
    """
    def __init__(self, base_recorder: DataRecorder) -> None:
        self._base_recorder = base_recorder

    def save(self, reading: SensorReading) -> None:
        # 1. Emitir el log estructurado en JSON
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": "INFO",
            "event": "sensor_reading_processed",
            "sensor_id": reading.sensor_id,
            "value": reading.value
        }
        logger.info(json.dumps(log_entry))
        
        # 2. Delegar el guardado real al grabador base
        self._base_recorder.save(reading)
        

##########################################################################
# from models import SensorReading (nuestro modelo inmutable)

# 1. El Contrato (ISP y DIP)
class DataRecorder(Protocol):
    """
    Define la regla: todo grabador debe tener un método 'save'
    que reciba un SensorReading inmutable.
    """
    def save(self, reading: SensorReading) -> None: ...

# 2. La Implementación para Tests (SRP y LSP)
class InMemoryRecorder:
    """
    Simula una base de datos o archivo en RAM.
    Perfecto para que nuestro test se ejecute en milisegundos.
    """
    def __init__(self) -> None:
        # Guardamos el historial de lecturas en una lista
        self.history: list[SensorReading] = []

    def save(self, reading: SensorReading) -> None:
        self.history.append(reading)

# 3. (Opcional) La Implementación para Producción
class CSVRecorder:
    """
    Un grabador real que podrías usar cuando conectes el sensor físico.
    """
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath
        
    def save(self, reading: SensorReading) -> None:
        # Lógica real para abrir un archivo y escribir la línea CSV
        with open(self._filepath, "a") as f:
            f.write(f"{reading.sensor_id},{reading.value}\n")
#####################################################

# 1. El Contrato (ISP y DIP)
class UARTDevice(Protocol):
    """
    Define cómo debe comportarse cualquier conexión serial.
    Interfaz segregada: solo expone el método necesario para leer.
    """
    def read_line(self) -> str: ...

# 2. La Implementación Simulada (El mock para tu Test)
class MockUARTDevice:
    """
    Simula el hardware. No requiere PySerial ni placas conectadas.
    Es lo que inyectaremos en la prueba unitaria para que pase.
    """
    def read_line(self) -> str:
        # Simulamos una trama de texto llegando por el pin RX
        return '{"id": "UART_01", "val": 25.4}'

# 3. La Implementación para Producción (LSP y OCP)
class RealUARTDevice:
    """
    Esta es la clase que usarías en producción con tu hardware físico.
    """
    def __init__(self, port: str, baudrate: int) -> None:
        # Aquí sí importarías e inicializarías 'serial.Serial'
        pass
        
    def read_line(self) -> str:
        # Lógica real para leer del buffer del puerto COM/ttyUSB
        # return self.serial.readline().decode('utf-8')
        pass
