import pytest

from app.domain.alert_status import VALID_STATUSES, validate_status_transition


@pytest.mark.parametrize("status", ["open", "acknowledged", "resolved"])
def test_valid_status_is_accepted(status: str) -> None:
    validate_status_transition(status)  # no debe lanzar


def test_invalid_status_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Estado invalido"):
        validate_status_transition("cerrado")


def test_valid_statuses_constant_has_exactly_three_values() -> None:
    assert VALID_STATUSES == {"open", "acknowledged", "resolved"}