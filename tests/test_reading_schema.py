import pytest
from pydantic import ValidationError

from app.schemas.reading_schema import ReadingCreate, ReadingUpdate


@pytest.mark.parametrize(
    "value,unit",
    [
        (-273.15, "C"),
        (-459.67, "F"),
        (0.0, "K"),
        (0.0, "%"),
        (100.0, "%"),
        (0.0, "hPa"),
    ],
)
def test_reading_create_valid_boundary(value: float, unit: str) -> None:
    reading = ReadingCreate(value=value, unit=unit)
    assert reading.value == value


@pytest.mark.parametrize(
    "value,unit",
    [
        (-273.16, "C"),
        (-459.68, "F"),
        (-0.01, "K"),
        (-0.01, "%"),
        (100.01, "%"),
        (-0.01, "hPa"),
    ],
)
def test_reading_create_below_boundary_fails(value: float, unit: str) -> None:
    with pytest.raises(ValidationError):
        ReadingCreate(value=value, unit=unit)


def test_reading_update_skips_physics_if_only_value_given() -> None:
    update = ReadingUpdate(value=-300.0)
    assert update.value == -300.0


def test_reading_update_validates_physics_if_both_given() -> None:
    with pytest.raises(ValidationError):
        ReadingUpdate(value=-300.0, unit="C")