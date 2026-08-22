from fastapi.testclient import TestClient


def test_stats_returns_min_max_avg(client: TestClient) -> None:
    sensor = client.post(
        "/sensors", json={"name": "Sensor Stats", "type": "temperature"}
    )
    sensor_id = sensor.json()["id"]
    for value in [10.0, 20.0, 30.0]:
        client.post(
            f"/sensors/{sensor_id}/readings", json={"value": value, "unit": "C"}
        )

    response = client.get(f"/sensors/{sensor_id}/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["minimum"] == 10.0
    assert body["maximum"] == 30.0
    assert body["average"] == 20.0


def test_stats_no_readings_returns_422(client: TestClient) -> None:
    sensor = client.post(
        "/sensors", json={"name": "Sensor Vacio", "type": "temperature"}
    )
    sensor_id = sensor.json()["id"]
    response = client.get(f"/sensors/{sensor_id}/stats")
    assert response.status_code == 422