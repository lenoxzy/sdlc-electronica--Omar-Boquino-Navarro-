
class SensorNotFoundError(Exception):
    pass
# diccionario para guardar los sensores 
class SensorRegistry:
    def __init__(self):
        self._sensors = {}

    def get(self, sensor_id: str):
        # Verificamos si realmente existe en el diccionario
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"El sensor {sensor_id} no fue encontrado.")
        return self._sensors[sensor_id]