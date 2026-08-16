from datetime import datetime

from app.domain.physics import validate_physics
from app.repositories.reading_repo import ReadingModel, ReadingRepository
from app.services.alert_service import AlertService
from app.services.exceptions import ReadingNotFoundError


class ReadingService:
    def __init__(
        self,
        repo: ReadingRepository,
        alert_service: AlertService | None = None,
    ) -> None:
        self._repo = repo
        self._alert_service = alert_service

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        validate_physics(value, unit)
        reading = self._repo.add(sensor_id, value, unit)
        if self._alert_service is not None:
            self._alert_service.evaluate(reading)
        return reading

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
        if (
            parsed_from is not None
            and parsed_to is not None
            and parsed_from > parsed_to
        ):
            raise ValueError("'from' no puede ser posterior a 'to'")
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
        current = self.get_reading(reading_id)  # 404 si no existe

        # Valida el resultado EFECTIVO del patch, no solo los campos que
        # llegaron: cubre cambiar solo "value" (unit se mantiene) y
        # también cambiar solo "unit" (el value existente podría dejar
        # de ser válido para la nueva unidad).
        effective_value = value if value is not None else current.value
        effective_unit = unit if unit is not None else current.unit
        validate_physics(effective_value, effective_unit)

        updated = self._repo.update(reading_id, value=value, unit=unit)
        if not updated:
            raise ReadingNotFoundError(f"Lectura con ID {reading_id} no encontrada")
        return updated

    def delete_reading(self, reading_id: int) -> None:
        deleted = self._repo.delete(reading_id)
        if not deleted:
            raise ReadingNotFoundError(f"Lectura con ID {reading_id} no encontrada")

    @staticmethod
    def _parse_date(value: str | None, field_name: str) -> datetime | None:
        if value is None:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(
                f"Formato de fecha invalido en '{field_name}': "
                f"se espera ISO 8601 (ej. 2026-01-01)"
            ) from None