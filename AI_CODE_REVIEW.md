Revisa esta clase como un ingeniero senior en un code review.
Busca: violaciones de SOLID, casos borde sin manejar, riesgos de seguridad
y problemas de rendimiento. Para cada hallazgo indica la linea y propon una correccion. No reescribas todo; solo senala.

# AI Code Review — ReadingService (Semana 5, Día 3)

Clase revisada: `app/services/reading_service.py`

## Hallazgos

| # | Línea | Hallazgo | Decisión |
|---|---|---|---|
| F1 | 13-15 | Validación física duplicada e incompleta en `record()` | Aceptado — extraída a `app/domain/physics.py`, reusada por schema y servicio |
| F2 | 42-49 | `update_reading()` no valida física en patches parciales; hueco confirmado en ambas direcciones (solo value, o solo unit) | Aceptado — corrección crítica|
| F3 | 45, 52 | Llamada redundante a `get_reading()` antes de update/delete | Aceptado solo para `delete_reading()`. Para `update_reading()`, la llamada se vuelve necesaria una vez corregido F2 (se necesita el valor/unidad actuales para validar el resultado efectivo del patch) |
| F4 | 60-61 | `_parse_date` no valida `from <= to` | Aceptado — se agrega chequeo explícito en `list_for_sensor` |
| F5 | 13 | NaN/Infinity no manejados explícitamente | Rechazado — Pydantic v2 rechaza esos tokens en el parseo JSON antes de llegar al servicio; no es alcanzable en la práctica |
| Edge case extra | — | `sensor_id` no convertible a int | Rechazado — ya lo previene el tipado `id: int` en el router |
| Edge case extra | — | PATCH con ambos campos `None` | Rechazado como bug — es un no-op idempotente válido para PATCH |
| Edge case extra | — | PATCH de solo `unit` con `value` actual inválido para la nueva unidad  — mismo fix que F2 lo cubre |