from fastapi.testclient import TestClient


def test_metrics_endpoint_returns_counts(client: TestClient) -> None:
    sensor = client.post(
        "/sensors", json={"name": "Sensor Metricas", "type": "temperature"}
    )
    sensor_id = sensor.json()["id"]
    client.post(
        f"/sensors/{sensor_id}/readings", json={"value": 20.0, "unit": "C"}
    )

    response = client.get("/metrics")
    assert response.status_code == 200
    body = response.json()
    assert body["total_sensors"] >= 1
    assert body["total_readings"] >= 1
    assert "total_alerts" in body