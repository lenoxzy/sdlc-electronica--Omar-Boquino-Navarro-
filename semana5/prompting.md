
# Tarea 1: función de conversión Celsius → Fahrenheit

### Prompt pobre
> "hazme una función que convierta temperatura"

### Resultado (prompt pobre)
```python
def convertir(temp):
    return temp * 9/5 + 32
```

### Prompt bueno
> CONTEXTO: API FastAPI (Python 3.12) para SensorHub, gestión de sensores IoT. Sigue arquitectura en capas con type hints estrictos verificados por mypy en modo estricto.
> TAREA: escribe una función pura celsius_to_fahrenheit(celsius: float) -> float en app/utils/conversions.py.
> RESTRICCIONES: type hints completos, docstring en español, sin dependencias externas, redondeo a 2 decimales con round().
> ENTREGA: solo la función, sin explicación adicional.

### Resultado (prompt bueno)
```python
def celsius_to_fahrenheit(celsius: float) -> float:
    """Convierte una temperatura de grados Celsius a Fahrenheit.

    Args:
        celsius: temperatura en grados Celsius.

    Returns:
        La temperatura equivalente en grados Fahrenheit, redondeada a 2 decimales.
    """
    return round((celsius * 9 / 5) + 32, 2)
```

### Diferencia
El prompt pobre no especifica unidades en el nombre (`convertir` de qué a qué), no tiene type hints (falla mypy estricto), no tiene docstring, y no dice dónde vive el archivo. El bueno produce algo listo para pegar directo en el proyecto y pasar CI sin ajustes.

---

# Tarea 2: detección de anomalías (lógica pura, testeable)

### Prompt pobre
> "necesito detectar si algo está mal con las lecturas"

### Resultado (prompt pobre)
```python
def check(readings):
    for r in readings:
        if r > 100:
            print("alerta!")
```

### Prompt bueno
> CONTEXTO: SensorHub, dominio de sensores. Necesito lógica pura de detección de anomalías, sin tocar FastAPI ni la base de datos, para poder testearla con un repositorio fake (mismo patrón que ya uso en ReadingService).
> TAREA: escribe una función is_anomalous(value: float, threshold: float) -> bool en app/services/anomaly.py que determine si una lectura supera el umbral configurado para su sensor.
> RESTRICCIONES: type hints completos, sin imports de FastAPI/SQLAlchemy, sin efectos secundarios (no imprime ni loggea).
> ENTREGA: solo la función, con un docstring breve.

### Resultado (prompt bueno)
```python
def is_anomalous(value: float, threshold: float) -> bool:
    """Determina si una lectura supera el umbral de alerta configurado.

    Args:
        value: valor de la lectura del sensor.
        threshold: umbral configurado para ese sensor.

    Returns:
        True si el valor supera el umbral, False en caso contrario.
    """
    return value > threshold
```

### Diferencia
El prompt pobre generó código con umbral fijo hardcodeado (100), efecto secundario (`print` en vez de retornar), y sin type hints — imposible de testear en aislamiento. El bueno es una función pura, parametrizada, que se puede probar sin base de datos ni servidor — y sienta la base para RF-4 (detección de anomalías) del proyecto final.

---

# Tarea 3: tests para la validación física de ReadingCreate/ReadingUpdate

### Prompt pobre
> "hazme tests para mi schema"

### Resultado (prompt pobre)
```python
def test_reading_create():
    r = ReadingCreate(value=10, unit="C")
    assert r.value == 10
```

### Prompt bueno
> CONTEXTO: ReadingCreate y ReadingUpdate (Pydantic v2) en app/schemas/reading_schema.py validan física real: cero absoluto para C/F/K, rango 0-100 para humedad (%), presión no negativa (hPa). Actualmente reading_schema.py tiene 58% de cobertura porque los validators no están probados con casos borde.
> TAREA: escribe tests pytest en tests/test_reading_schema.py que cubran, para cada unidad (C, F, K, %, hPa): un valor válido en el límite, y un valor justo por debajo del límite que debe lanzar ValidationError.
> RESTRICCIONES: usa pytest.raises(ValidationError), no dupliques casos entre ReadingCreate y ReadingUpdate salvo que el comportamiento difiera (ReadingUpdate valida física solo si vienen AMBOS campos).
> ENTREGA: solo el código de los tests.

### Resultado (prompt bueno)
```python
import pytest
from pydantic import ValidationError

from app.schemas.reading_schema import ReadingCreate, ReadingUpdate


@pytest.mark.parametrize(
    "value,unit",
    [
        (-273.15, "C"),
        (-459.67, "F"),
        (0.0, "K"),
        (0.0, "%"),
        (100.0, "%"),
        (0.0, "hPa"),
    ],
)
def test_reading_create_valid_boundary(value: float, unit: str) -> None:
    reading = ReadingCreate(value=value, unit=unit)
    assert reading.value == value


@pytest.mark.parametrize(
    "value,unit",
    [
        (-273.16, "C"),
        (-459.68, "F"),
        (-0.01, "K"),
        (-0.01, "%"),
        (100.01, "%"),
        (-0.01, "hPa"),
    ],
)
def test_reading_create_below_boundary_fails(value: float, unit: str) -> None:
    with pytest.raises(ValidationError):
        ReadingCreate(value=value, unit=unit)


def test_reading_update_skips_physics_if_only_value_given() -> None:
    update = ReadingUpdate(value=-300.0)
    assert update.value == -300.0


def test_reading_update_validates_physics_if_both_given() -> None:
    with pytest.raises(ValidationError):
        ReadingUpdate(value=-300.0, unit="C")
```

### Diferencia
El prompt pobre produjo un solo test trivial de camino feliz — no mueve la aguja de cobertura real. El bueno produjo 14 casos parametrizados que cubren el límite exacto y el punto justo debajo para las 5 unidades, más el caso borde de ReadingUpdate (que solo valida física si llegan ambos campos). Este resultado sí cierra el hueco de cobertura real del proyecto.