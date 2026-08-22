from fastapi.testclient import TestClient


def test_create_sensor_success(client: TestClient) -> None:
    response = client.post(
        "/sensors",
        json={"name": "Sensor Norte", "type": "temperature", "location": "Bodega 1"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Sensor Norte"


def test_create_sensor_without_location(client: TestClient) -> None:
    response = client.post("/sensors", json={"name": "Sensor Sur", "type": "humidity"})
    assert response.status_code == 201
    assert response.json()["location"] is None


def test_list_sensors_empty(client: TestClient) -> None:
    response = client.get("/sensors")
    assert response.status_code == 200
    assert response.json() == []


def test_list_sensors_returns_created(client: TestClient) -> None:
    client.post("/sensors", json={"name": "Sensor A", "type": "temperature"})
    client.post("/sensors", json={"name": "Sensor B", "type": "humidity"})
    response = client.get("/sensors")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_sensor_by_id_success(client: TestClient) -> None:
    created = client.post("/sensors", json={"name": "Sensor C", "type": "temperature"})
    sensor_id = created.json()["id"]
    response = client.get(f"/sensors/{sensor_id}")
    assert response.status_code == 200
    assert response.json()["id"] == sensor_id


def test_get_sensor_not_found(client: TestClient) -> None:
    response = client.get("/sensors/999")
    assert response.status_code == 404


def test_delete_sensor_success(client: TestClient) -> None:
    created = client.post("/sensors", json={"name": "Sensor D", "type": "temperature"})
    sensor_id = created.json()["id"]
    response = client.delete(f"/sensors/{sensor_id}")
    assert response.status_code == 204

    # Soft-delete: el sensor ya no aparece en el listado activo...
    listed = client.get("/sensors").json()
    assert not any(s["id"] == sensor_id for s in listed)

    # ...pero el registro sigue existiendo y consultable individualmente,
    # marcado como inactivo.
    detail = client.get(f"/sensors/{sensor_id}")
    assert detail.status_code == 200
    assert detail.json()["is_active"] is False


def test_delete_sensor_not_found(client: TestClient) -> None:
    response = client.delete("/sensors/999")
    assert response.status_code == 404