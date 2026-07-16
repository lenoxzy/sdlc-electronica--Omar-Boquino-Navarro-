from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Any  
import json

# ==============================================================================
# DEFINICIÓN DE ESTRUCTURAS DE DATOS
# ==============================================================================

class SensorType(Enum):            
    """
    Enumera los tipos de sensores permitidos. 
    Usar 'auto()' le asigna un valor interno automático. Esto evita usar strings 
    como "temp" o "temperatura", los cuales son propensos a errores de tipeo.
    """
    TEMPERATURE = auto()
    HUMIDITY = auto()
 
@dataclass(frozen=True)            
class lectura:
    """
    Representa una única medición de un sensor.
    'frozen=True' la hace inmutable: una vez instanciada, sus valores no pueden 
    ser reasignados (ej. no puedes hacer mi_lectura.value = 10).
    """
    sensor_id: str
    value: float
    sensor_type: SensorType


# ==============================================================================
# FUNCIONES PURAS
# ==============================================================================

# 1. CONVERSIÓN DE UNIDADES (Temperatura de Celsius a Fahrenheit)
def celsius_a_fahrenheit(r: lectura) -> lectura:
    """
    Recibe una lectura en grados Celsius y devuelve una nueva instancia 
    con el valor convertido a Fahrenheit.
    """
    # Si la lectura no es de temperatura, la devuelve intacta por seguridad
    if r.sensor_type != SensorType.TEMPERATURE:
        return r
        
    # Realiza la conversión matemática
    fahrenheit_val = (r.value * 9 / 5) + 32
    
    # Retorna un objeto NUEVO con el valor convertido y redondeado a 2 decimales
    return lectura(
        sensor_id=r.sensor_id,
        value=round(fahrenheit_val, 2),
        sensor_type=r.sensor_type
    )
# 2. DETECCIÓN DE UMBRAL (Alertas rápidas)
def check_threshold(r: lectura, max_limit: float) -> bool:
    """
    Compara el valor de la lectura con un límite máximo.
    Retorna True si el valor supera el umbral 
    """
    return r.value > max_limit

# 3. SERIALIZACIÓN (Conversión a Diccionario nativo)
def to_dict(r: lectura) -> Dict[str, Any]:
    """
    Convierte la estructura 'lectura' a un diccionario estándar de Python.
    Esto es el paso previo necesario para poder guardarlo en bases de datos 
    o enviarlo por la red.
    """
    return {
        "sensor_id": r.sensor_id,
        "value": r.value,
        # '.name' extrae el texto del Enum (ej. "TEMPERATURE" en vez del objeto)
        "sensor_type": r.sensor_type.name 
    }
# 4. SERIALIZACIÓN (Conversión a string JSON)
def to_json_string(r: lectura) -> str: 
    """
    Convierte la lectura a un formato de texto JSON (String).
    Se apoya en la función 'to_dict' para transformar los datos antes de 
    serializarlos con json.dumps().
    """
    return json.dumps(to_dict(r))

# 5. TRANSFORMACIÓN / CALIBRACIÓN (Corrección por desvío/offset)
def apply_offset(r: lectura, offsets: Dict[str, float]) -> lectura:
    """
    Aplica una corrección (calibración) al valor del sensor.
    Busca en un diccionario de 'offsets' usando el ID del sensor.
    """
    # Busca si hay un offset guardado para este sensor_id. 
    # Si no lo encuentra, asume que el offset es 0.0 (no hay error).
    offset: float = offsets.get(r.sensor_id, 0.0)
    
    # Optimización: si no hay que calibrar, devolvemos la lectura original
    if offset == 0.0:
        return r
        
    # Si hay offset, creamos y retornamos una nueva lectura ajustada
    return lectura(
        sensor_id=r.sensor_id,
        value=r.value + offset,
        sensor_type=r.sensor_type
    )
