from app.repositories.reading_repo import ReadingModel, ReadingRepository
from app.services.exceptions import ReadingNotFoundError, SensorNotFoundError

class ReadingService:
    """Lógica de negocio. Depende de la abstracción del repositorio (DIP)."""

    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        if value < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")
        return self._repo.add(sensor_id, value, unit)

    def list_for_sensor(
        self, 
        sensor_id: str, 
        limit: int = 50, 
        offset: int = 0, 
        from_date: str | None = None, 
        to_date: str | None = None
    ) -> list[ReadingModel]:
        # El router llama a este método público, ocultando "_repo"
        return self._repo.list_for_sensor(
            sensor_id=sensor_id, 
            limit=limit, 
            offset=offset, 
            from_date=from_date, 
            to_date=to_date
        )

    def get_reading(self, reading_id: int) -> ReadingModel:
        reading = self._repo.get_by_id(reading_id)
        if not reading:
            # Levantamos la excepción de dominio que creamos
            raise ReadingNotFoundError(f"Lectura con ID {reading_id} no encontrada")
        return reading

    def update_reading(self, reading_id: int, value: float | None = None, unit: str | None = None) -> ReadingModel:
        # Reutilizamos get_reading para asegurar que exista (levanta 404 si no)
        self.get_reading(reading_id)
        
        # Delegamos la actualización al repositorio
        updated_reading = self._repo.update(reading_id, value, unit)
        return updated_reading

    def delete_reading(self, reading_id: int) -> None:
        # Comprobamos que existe antes de intentar borrar
        self.get_reading(reading_id)
        
        # Delegamos el borrado físico al repositorio 
        self._repo.delete(reading_id)