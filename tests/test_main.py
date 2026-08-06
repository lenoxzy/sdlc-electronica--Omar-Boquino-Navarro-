from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool  # <--- NUEVO IMPORT

from app.db import Base
from app.main import app
from app.models import models
from app.routers.reading_router import get_db

# 1. Creamos el motor en RAM asegurando que todas las conexiones compartan las tablas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # <--- LA MAGIA ESTÁ AQUÍ
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# 2. Le decimos a FastAPI que use nuestra BD en RAM
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


# 3. Fixture de base de datos
@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    # Usamos el modelo sin las propiedades nuevas para que no marque TypeError
    nuevo_sensor = models.Sensor(id=1, name="Sensor Test")
    db.add(nuevo_sensor)
    db.commit()
    db.close()

    yield

    Base.metadata.drop_all(bind=engine)

# --- 4. LAS PRUEBAS ---

def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "connected"}


def test_list_readings_empty() -> None:
    # Como la BD en RAM siempre está nueva, debe regresar lista vacía
    response = client.get("/sensors/1/readings")
    assert response.status_code == 200
    assert response.json() == []


def test_create_reading_success() -> None:
    # Creamos un registro real en la BD en RAM
    response = client.post("/sensors/1/readings", json={"value": 28.0, "unit": "C"})
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["value"] == 28.0


def test_create_reading_fails_absolute_zero() -> None:
    # Tu nuevo y poderoso Pydantic V2 ataja este error
    response = client.post("/sensors/1/readings", json={"value": -300.0, "unit": "C"})
    assert response.status_code == 422
    assert "cero absoluto" in str(response.json()["detail"])


def test_create_reading_sensor_not_found() -> None:
    response = client.post("/sensors/999/readings", json={"value": 25.0, "unit": "C"})
    assert response.status_code == 404