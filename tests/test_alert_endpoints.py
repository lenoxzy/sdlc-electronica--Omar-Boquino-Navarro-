from fastapi.testclient import TestClient


def test_reading_over_threshold_creates_alert(client: TestClient) -> None:
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor G",
            "type": "temperature",
            "alert_threshold": 30.0,
        },
    )
    sensor_id = sensor.json()["id"]

    client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 45.0, "unit": "C"}
    )

    response = client.get(f"/sensors/{sensor_id}/alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) == 1
    assert alerts[0]["value"] == 45.0


def test_reading_within_threshold_creates_no_alert(
    client: TestClient,
) -> None:
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor H",
            "type": "temperature",
            "alert_threshold": 100.0,
        },
    )
    sensor_id = sensor.json()["id"]

    client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 20.0, "unit": "C"}
    )

    response = client.get(f"/sensors/{sensor_id}/alerts")
    assert response.json() == []


def test_sensor_without_threshold_never_creates_alert(
    client: TestClient,
) -> None:
    sensor = client.post(
        "/sensors", json={"name": "Sensor I", "type": "temperature"}
    )
    sensor_id = sensor.json()["id"]

    client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 999.0, "unit": "C"}
    )

    response = client.get(f"/sensors/{sensor_id}/alerts")
    assert response.json() == []


def test_list_all_alerts_endpoint(client: TestClient) -> None:
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor J",
            "type": "temperature",
            "alert_threshold": 10.0,
        },
    )
    sensor_id = sensor.json()["id"]
    client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 50.0, "unit": "C"}
    )

    response = client.get("/alerts")
    assert response.status_code == 200
    assert len(response.json()) >= 1