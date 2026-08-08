from fastapi.testclient import TestClient


def _create_sensor(client: TestClient) -> int:
    response = client.post("/sensors", json={"name": "Sensor E", "type": "temperature"})
    return int(response.json()["id"])


def _create_reading(client: TestClient, sensor_id: int) -> int:
    response = client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 22.5, "unit": "C"}
    )
    return int(response.json()["id"])

def test_get_reading_success(client: TestClient) -> None:
    sensor_id = _create_sensor(client)
    reading_id = _create_reading(client, sensor_id)
    response = client.get(f"/readings/{reading_id}")
    assert response.status_code == 200 asdfasf
    assert response.json()["id"] == reading_id


def test_get_reading_not_found(client: TestClient) -> None:
    assert client.get("/readings/999").status_code == 404


def test_update_reading_success(client: TestClient) -> None:
    sensor_id = _create_sensor(client)
    reading_id = _create_reading(client, sensor_id)
    response = client.patch(f"/readings/{reading_id}", json={"value": 30.0})
    assert response.status_code == 200
    assert response.json()["value"] == 30.0


def test_update_reading_not_found(client: TestClient) -> None:
    assert client.patch("/readings/999", json={"value": 30.0}).status_code == 404


def test_delete_reading_success(client: TestClient) -> None:
    sensor_id = _create_sensor(client)
    reading_id = _create_reading(client, sensor_id)
    assert client.delete(f"/readings/{reading_id}").status_code == 204
    assert client.get(f"/readings/{reading_id}").status_code == 404


def test_delete_reading_not_found(client: TestClient) -> None:
    assert client.delete("/readings/999").status_code == 404