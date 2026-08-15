from fastapi.testclient import TestClient


def _create_sensor(client: TestClient) -> int:
    response = client.post("/sensors", json={"name": "Sensor F", "type": "temperature"})
    return int(response.json()["id"])


def _create_reading(client: TestClient, sensor_id: int, value: float, unit: str) -> int:
    response = client.post(
        f"/sensors/{sensor_id}/readings", json={"value": value, "unit": unit}
    )
    assert response.status_code == 201
    return int(response.json()["id"])


def test_update_only_value_rejects_invalid_physics(client: TestClient) -> None:
    """PATCH con solo 'value' debe validar contra la unidad ya guardada."""
    sensor_id = _create_sensor(client)
    reading_id = _create_reading(client, sensor_id, value=20.0, unit="C")
    response = client.patch(f"/readings/{reading_id}", json={"value": -300.0})
    assert response.status_code == 422


def test_update_only_unit_rejects_now_invalid_value(client: TestClient) -> None:
    """PATCH de solo 'unit' valida el value existente contra la nueva unidad."""
    sensor_id = _create_sensor(client)
    reading_id = _create_reading(client, sensor_id, value=150.0, unit="hPa")
    response = client.patch(f"/readings/{reading_id}", json={"unit": "%"})
    assert response.status_code == 422


def test_update_both_fields_valid_combination_succeeds(client: TestClient) -> None:
    sensor_id = _create_sensor(client)
    reading_id = _create_reading(client, sensor_id, value=50.0, unit="hPa")
    response = client.patch(
        f"/readings/{reading_id}", json={"value": 60.0, "unit": "%"}
    )
    assert response.status_code == 200
    assert response.json()["value"] == 60.0


def test_list_readings_from_after_to_rejected(client: TestClient) -> None:
    sensor_id = _create_sensor(client)
    response = client.get(
        f"/sensors/{sensor_id}/readings",
        params={"from": "2026-06-01", "to": "2026-01-01"},
    )
    assert response.status_code == 422


def test_delete_reading_not_found_after_refactor(client: TestClient) -> None:
    """Regresión: delete_reading ya no llama a get_reading() primero."""
    response = client.delete("/readings/999")
    assert response.status_code == 404


def test_record_rejects_kelvin_below_zero(client: TestClient) -> None:
    """Cobertura nueva: la validación compartida ahora también se
    ejercita en record(), no solo en el schema."""
    sensor_id = _create_sensor(client)
    response = client.post(
        f"/sensors/{sensor_id}/readings", json={"value": -5.0, "unit": "K"}
    )
    assert response.status_code == 422