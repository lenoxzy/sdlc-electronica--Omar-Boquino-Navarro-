VALID_STATUSES = {"open", "acknowledged", "resolved"}


def validate_status_transition(status: str) -> None:
    """Valida que el estado sea uno de los permitidos para una alerta.

    Raises:
        ValueError: si el estado no pertenece a VALID_STATUSES.
    """
    if status not in VALID_STATUSES:
        raise ValueError(
            f"Estado invalido: '{status}'. Debe ser uno de: {sorted(VALID_STATUSES)}"
        )