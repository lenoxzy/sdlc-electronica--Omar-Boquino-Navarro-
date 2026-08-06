from datetime import datetime

from app.repositories.reading_repo import ReadingModel, ReadingRepository
from app.services.exceptions import ReadingNotFoundError


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
        to_date: str | None = None,
    ) -> list[ReadingModel]:
        parsed_from = self._parse_date(from_date, "from")
        parsed_to = self._parse_date(to_date, "to")
        return self._repo.list_for_sensor(
            sensor_id=sensor_id,
            limit=limit,
            offset=offset,
            from_date=parsed_from,
            to_date=parsed_to,
        )

    def get_reading(self, reading_id: int) -> ReadingModel:
        reading = self._repo.get(reading_id)
        if not reading:
            raise ReadingNotFoundError(f"Lectura con ID {reading_id} no encontrada")
        return reading

    def update_reading(
        self, reading_id: int, value: float | None = None, unit: str | None = None
    ) -> ReadingModel:
        self.get_reading(reading_id)  # valida existencia -> 404 si no existe
        updated = self._repo.update(reading_id, value=value, unit=unit)
        if not updated:
            raise ReadingNotFoundError(f"Lectura con ID {reading_id} no encontrada")
        return updated

    def delete_reading(self, reading_id: int) -> None:
        self.get_reading(reading_id)
        self._repo.delete(reading_id)

    @staticmethod
    def _parse_date(value: str | None, field_name: str) -> datetime | None:
        if value is None:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(
                f"Formato de fecha invalido en '{field_name}': se espera ISO 8601 (ej. 2026-01-01)"
            ) from None