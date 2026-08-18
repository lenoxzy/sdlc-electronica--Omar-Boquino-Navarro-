"""Reglas físicas compartidas por el schema (Pydantic) y el servicio.

Única fuente de verdad de qué valores son físicamente posibles por unidad,
para no repetir (e inconsistentemente) la misma lógica en dos capas.
"""

_ABSOLUTE_ZERO: dict[str, float] = {"C": -273.15, "F": -459.67, "K": 0.0}


def validate_physics(value: float, unit: str) -> None:
    """Valida que un valor sea físicamente posible para su unidad.

    Raises:
        ValueError: si el valor viola un límite físico conocido.
    """
    if unit in _ABSOLUTE_ZERO and value < _ABSOLUTE_ZERO[unit]:
          raise ValueError(
            f"El valor no puede ser menor al cero absoluto "
            f"({_ABSOLUTE_ZERO[unit]} {unit})"
        )
    if unit == "%" and not (0 <= value <= 100):
        raise ValueError("La humedad debe estar entre 0% y 100%")
    if unit == "hPa" and value < 0:
        raise ValueError("La presión no puede ser negativa")