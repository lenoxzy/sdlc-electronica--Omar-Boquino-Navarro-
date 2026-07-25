# registry.py

class SensorNotFoundError(Exception):
    pass

class SensorRegistry:
    def get(self, sensor_id: str):
        # El código mínimo para que pase el test
        raise SensorNotFoundError(f"El sensor {sensor_id} no fue encontrado.")