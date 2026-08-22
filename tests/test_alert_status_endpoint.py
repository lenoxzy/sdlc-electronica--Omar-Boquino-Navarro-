from fastapi.testclient import TestClient


def _create_alert(client: TestClient, value: float = 99.0) -> int:
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor con alerta",
            "type": "temperature",
            "alert_threshold": 10.0,
        },
    )
    sensor_id = sensor.json()["id"]
    client.post(f"/sensors/{sensor_id}/readings", json={"value": value, "unit": "C"})
    alerts = client.get(f"/sensors/{sensor_id}/alerts").json()
    return int(alerts[0]["id"])


def test_new_alert_defaults_to_open(client: TestClient) -> None:
    sensor = client.post(
        "/sensors",
        json={"name": "Sensor A", "type": "temperature", "alert_threshold": 10.0},
    )
    sensor_id = sensor.json()["id"]
    client.post(f"/sensors/{sensor_id}/readings", json={"value": 99.0, "unit": "C"})
    alerts = client.get(f"/sensors/{sensor_id}/alerts").json()
    assert alerts[0]["status"] == "open"


def test_update_alert_status_to_acknowledged(client: TestClient) -> None:
    alert_id = _create_alert(client)
    response = client.patch(
        f"/alerts/{alert_id}/status", json={"status": "acknowledged"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "acknowledged"


def test_update_alert_status_invalid_value_rejected(client: TestClient) -> None:
    alert_id = _create_alert(client)
    response = client.patch(f"/alerts/{alert_id}/status", json={"status": "cerrado"})
    assert response.status_code == 422


def test_update_status_alert_not_found(client: TestClient) -> None:
    response = client.patch("/alerts/999/status", json={"status": "acknowledged"})
    assert response.status_code == 404