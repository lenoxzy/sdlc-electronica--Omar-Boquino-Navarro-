from fastapi.testclient import TestClient


def _create_sensor(client: TestClient) -> int:
    response = client.post(
        "/sensors",
        json={"name": "Sensor Test", "type": "temperature", "location": "Planta A"},
    )
    assert response.status_code == 201
    return int(response.json()["id"])


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_readings_empty(client: TestClient) -> None:
    sensor_id = _create_sensor(client)
    response = client.get(f"/sensors/{sensor_id}/readings")
    assert response.status_code == 200
    assert response.json() == []


def test_create_reading_success(client: TestClient) -> None:
    sensor_id = _create_sensor(client)
    response = client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 28.0, "unit": "C"}
    )
    assert response.status_code == 201
    assert response.json()["value"] == 28.0


def test_create_reading_fails_absolute_zero(client: TestClient) -> None:
    sensor_id = _create_sensor(client)
    response = client.post(
        f"/sensors/{sensor_id}/readings", json={"value": -300.0, "unit": "C"}
    )
    assert response.status_code == 422
    assert "cero absoluto" in str(response.json()["detail"])


def test_create_reading_sensor_not_found(client: TestClient) -> None:
    response = client.post("/sensors/999/readings", json={"value": 25.0, "unit": "C"})
    assert response.status_code == 404