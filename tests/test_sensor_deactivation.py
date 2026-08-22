from app.domain.sensor_status import deactivate_sensor


def test_deactivate_sensor_sets_is_active_false() -> None:
    result = deactivate_sensor(is_active=True)
    assert result is False


def test_deactivate_already_inactive_sensor_stays_false() -> None:
    result = deactivate_sensor(is_active=False)
    assert result is False