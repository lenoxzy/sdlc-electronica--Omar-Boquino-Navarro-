from dataclasses import dataclass


@dataclass
class ReadingStats:
    minimum: float
    maximum: float
    average: float


def calculate_stats(values: list[float]) -> ReadingStats:
    """Calcula min/max/promedio de una lista de valores de lectura.

    Raises:
        ValueError: si la lista está vacía.
    """
    if not values:
        raise ValueError("Se requiere al menos una lectura para calcular estadisticas")

    return ReadingStats(
        minimum=min(values),
        maximum=max(values),
        average=sum(values) / len(values),
    )