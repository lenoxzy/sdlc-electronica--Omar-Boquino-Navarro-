import random
from US_01 import SensorReading  # Ajusta el nombre si tu archivo es distinto

class SensorSimulator:
    """Simula hardware real generando datos con ruido gaussiano (campana de Gauss)."""
    
    def __init__(self, temp_promedio: float = 25.0, temp_variacion: float = 5.0,
                 hum_promedio: float = 60.0, hum_variacion: float = 10.0,
                 seed: int | None = None):
        if seed is not None:
            random.seed(seed)  # Semilla para que el test sea determinista (repetible)
            
        self._t_mu = temp_promedio
        self._t_sigma = temp_variacion
        self._h_mu = hum_promedio
        self._h_sigma = hum_variacion

    def read_sensor(self, sensor_id: str, reading_type: str) -> SensorReading:
        if reading_type == "temperature":
            valor = random.gauss(self._t_mu, self._t_sigma)
        elif reading_type == "humidity":
            valor = random.gauss(self._h_mu, self._h_sigma)
        else:
            raise ValueError(f"Tipo desconocido: {reading_type}")
            
        return SensorReading(sensor_id, round(valor, 2), reading_type)