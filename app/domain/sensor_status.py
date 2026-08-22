def deactivate_sensor(is_active: bool) -> bool:
    """Desactiva un sensor. Idempotente: desactivar uno ya inactivo
    no cambia nada ni lanza error."""
    return False