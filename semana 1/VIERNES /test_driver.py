import pytest
# 2. Importas las herramientas simuladas desde codigouni.py
from codigouni import MockUARTDevice, JSONUARTParser, InMemoryRecorder, UARTDevice, DataParser, DataRecorder, SensorReading, UARTDevice,CANParser, ThreadSafeCircularRecorder, JSONLoggingRecorderWrapper 

from dataclasses import dataclass, FrozenInstanceError
import json

class DriverModernizadoUART:
    def __init__(
        self, 
        device: UARTDevice, 
        parser: DataParser, 
        recorder: DataRecorder
    ) -> None:
        self._device = device
        self._parser = parser
        self._recorder = recorder
        
    def process_next_reading(self) -> None:
        raw_data = self._device.read_line()
        reading = self._parser.parse(raw_data)
        self._recorder.save(reading)


##########################################3
def test_driver_modernizado_uart() -> None: 
    """
    Verifica que el driver UART pueda leer una cadena de texto sin hardware físico...
    """
    # 1. PREPARAR (Arrange)
    device_simulado = MockUARTDevice()      
    parser_json = JSONUARTParser()          
    recorder_memoria = InMemoryRecorder()   
    
    driver = DriverModernizadoUART(
        device=device_simulado,
        parser=parser_json,
        recorder=recorder_memoria
    )
    
    # 2. ACTUAR (Act)
    driver.process_next_reading()
    
    # 3. VERIFICAR (Assert)
    assert len(recorder_memoria.history) == 1
    lectura_guardada = recorder_memoria.history[0]
    assert lectura_guardada.sensor_id == "UART_01"
    assert lectura_guardada.value == 25.4
##################################################################
import pytest
from dataclasses import dataclass, FrozenInstanceError
import json

# ==========================================
# EXTENSIONES PARA CUMPLIR LA RÚBRICA 
# (Configuración y Escritura JSON)
# ==========================================
@dataclass(frozen=True)
class UartConfig:
    """Valida el baudrate en el momento de su creación (SRP)."""
    baudrate: int
    
    def __post_init__(self) -> None:
        valid_baudrates = [9600, 19200, 38400, 115200]
        if self.baudrate not in valid_baudrates:
            raise ValueError(f"Baudrate {self.baudrate} inválido. Use estándar.")

class JSONRecorder:
    """Implementación de DataRecorder que escribe JSON-lines."""
    def __init__(self, filepath: str) -> None:
        self._filepath = filepath

    def save(self, reading: SensorReading) -> None:
        with open(self._filepath, "a", encoding="utf-8") as f:
            json.dump({"sensor_id": reading.sensor_id, "value": reading.value}, f)
            f.write("\n")

# ==========================================
# LA BATERÍA DE TESTS (Rúbrica Día 5)
# ==========================================

# --- GRUPO 1: Modelos y Configuración (Inmutabilidad y Baudrate) ---

def test_sensor_reading_es_inmutable() -> None:
    """Verifica que un dato crudo no pueda ser alterado por error."""
    lectura = SensorReading(sensor_id="T1", value=20.5)
    with pytest.raises(FrozenInstanceError):
        lectura.value = 25.0  # Intentar reasignar lanza error de dataclass frozen

def test_uart_config_rechaza_baudrate_invalido() -> None:
    """Verifica la validación física de la configuración del puerto."""
    with pytest.raises(ValueError, match="inválido"):
        UartConfig(baudrate=9999)

def test_uart_config_es_inmutable() -> None:
    """Garantiza que la configuración del puerto no cambie en tiempo de ejecución."""
    config = UartConfig(baudrate=115200)
    with pytest.raises(FrozenInstanceError):
        config.baudrate = 9600

# --- GRUPO 2: Parsers (Frames válidos e inválidos) ---

def test_json_parser_decodifica_frame_valido() -> None:
    """Verifica el caso de éxito (happy path)."""
    parser = JSONUARTParser()
    lectura = parser.parse('{"id": "SENS_01", "val": 15.2}')
    assert lectura.sensor_id == "SENS_01"
    assert lectura.value == 15.2

def test_json_parser_rechaza_frame_invalido() -> None:
    """Verifica la robustez ante ruido en el cable (JSON roto)."""
    parser = JSONUARTParser()
    with pytest.raises(ValueError, match="Trama UART corrupta"):
        parser.parse('{"id": "SENS_01", "val": ')  # Falta cerrar llaves

def test_json_parser_asigna_valores_por_defecto_si_faltan_datos() -> None:
    """Verifica el comportamiento ante un frame incompleto."""
    parser = JSONUARTParser()
    lectura = parser.parse('{"id": "SENS_02"}')  # No envía valor
    assert lectura.value == 0.0

# --- GRUPO 3: Hardware y Grabación (Dispositivo desconectado y JSON) ---

def test_dispositivo_desconectado_arroja_error() -> None:
    """Verifica el manejo de errores del hardware simulando una desconexión."""
    class DispositivoFalla(UARTDevice):
        def read_line(self) -> str:
            raise ConnectionError("Dispositivo UART no conectado")
            
    dispositivo = DispositivoFalla()
    with pytest.raises(ConnectionError, match="no conectado"):
        dispositivo.read_line()

def test_recorder_escribe_formato_json_correcto(tmp_path) -> None:
    """
    Verifica la escritura JSON. 
    Nota: 'tmp_path' es una herramienta nativa de pytest para crear 
    archivos temporales que se borran solos al terminar el test.
    """
    archivo_temp = tmp_path / "test_historial.jsonl"
    recorder = JSONRecorder(filepath=str(archivo_temp))
    lectura = SensorReading(sensor_id="ESP32", value=42.0)
    
    # Ejecutamos el guardado
    recorder.save(lectura)
    
    # Leemos el archivo físico recién creado para confirmar qué se guardó
    contenido = archivo_temp.read_text().strip()
    datos_guardados = json.loads(contenido)
    
    assert datos_guardados["sensor_id"] == "ESP32"
    assert datos_guardados["value"] == 42.0
###########################anexo de la extension#####################################
def test_driver_extension_alto_potencial() -> None:
    """
    Evalúa la extensión completa: Parser CAN, Buffer Thread-Safe y Logging JSON.
    """
    # 1. PREPARAR (Arrange)
    # Hardware que emite una trama CAN
    class MockCANDevice:
        def read_line(self) -> str:
            return "CAN_ID:MOTOR_01 VAL:88.5"
            
    device_can = MockCANDevice()
    parser_can = CANParser()
    
    # Grabador en memoria circular (capacidad máxima de 5)
    buffer_seguro = ThreadSafeCircularRecorder(max_size=5)
    
    # Envolvemos el buffer con nuestro logger JSON
    recorder_con_logging = JSONLoggingRecorderWrapper(base_recorder=buffer_seguro)
    
    # Ensamblamos el driver
    driver = DriverModernizadoUART(
        device=device_can,
        parser=parser_can,
        recorder=recorder_con_logging
    )
    
    # 2. ACTUAR (Act)
    driver.process_next_reading()
    
    # 3. VERIFICAR (Assert)
    historial = buffer_seguro.get_all()
    assert len(historial) == 1
    assert historial[0].sensor_id == "MOTOR_01"
    assert historial[0].value == 88.5
