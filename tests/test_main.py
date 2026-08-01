from fastapi.testclient import TestClient
from app.main import app, get_service
from app.services.reading_service import ReadingService
from app.repositories.reading_repo import ReadingModel

# 1. Creamos nuestro cliente de pruebas (simula un navegador o Postman)
client = TestClient(app)

# 2. Creamos un Repositorio Falso específico para probar la API
class MockAPIReadingRepository:
    def list_for_sensor(self, sensor_id: str) -> list[ReadingModel]:
        return [ReadingModel(id=1, sensor_id=sensor_id, value=25.5, unit="C")]
    
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        # Simulamos el error de la base de datos si el sensor no existe
        if sensor_id == "999":
            raise ValueError("Sensor no encontrado")
        return ReadingModel(id=2, sensor_id=sensor_id, value=value, unit=unit)

# 3. Sobrescribimos la dependencia de FastAPI
def override_get_service():
    return ReadingService(repo=MockAPIReadingRepository())

app.dependency_overrides[get_service] = override_get_service

# --- 4. LAS PRUEBAS DE LOS ENDPOINTS ---

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "connected"}

def test_list_readings_success():
    response = client.get("/sensors/1/readings")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["value"] == 25.5

def test_create_reading_success():
    response = client.post("/sensors/1/readings", json={"value": 28.0, "unit": "C"})
    assert response.status_code == 201
    assert response.json()["id"] == 2
    assert response.json()["value"] == 28.0

def test_create_reading_fails_absolute_zero():
    # Probamos la regla de negocio (Error 422)
    response = client.post("/sensors/1/readings", json={"value": -300.0, "unit": "C"})
    assert response.status_code == 422
    assert "cero absoluto" in response.json()["detail"]

def test_create_reading_sensor_not_found():
    # Probamos el error cuando el sensor no existe (Error 404)
    response = client.post("/sensors/999/readings", json={"value": 25.0, "unit": "C"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Sensor no encontrado"