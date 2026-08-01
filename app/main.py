from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db import SessionLocal, engine, Base
from app.services.reading_service import ReadingService
from app.repositories.reading_repo import SQLAlchemyReadingRepository

# Aseguramos que las tablas existan en la base de datos al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.1.0")

# --- 1. ESQUEMAS PYDANTIC (Capa de Presentación) ---
class ReadingCreate(BaseModel):
    value: float
    unit: str = "C"

class ReadingOut(BaseModel):
    id: int
    value: float
    unit: str

# --- 2. SISTEMA DE INYECCIÓN DE DEPENDENCIAS (El cableado) ---
def get_db():
    """Entrega la conexión a SQLite y la cierra al terminar la petición."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_service(db: Session = Depends(get_db)):
    """Inyecta la DB al repositorio, y el repositorio al servicio."""
    repo = SQLAlchemyReadingRepository(db)
    return ReadingService(repo=repo)

# --- 3. ENDPOINTS (Respetando la tabla REST) ---
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "db": "connected"}

@app.get("/sensors/{id}/readings", response_model=List[ReadingOut], status_code=200)
def list_readings(
    id: int,
    limit: int = 50,
    offset: int = 0,
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    service: ReadingService = Depends(get_service)
):
    """Listar lecturas de un sensor (con paginación y filtros de fecha)"""
    # Usamos el repositorio a través de la instancia del servicio
    readings = service._repo.list_for_sensor(sensor_id=str(id))
    return readings

@app.post("/sensors/{id}/readings", response_model=ReadingOut, status_code=201)
def create_reading(
    id: int,
    reading: ReadingCreate,
    service: ReadingService = Depends(get_service)
):
    """Crear una lectura para un sensor específico"""
    try:
        # El servicio valida la regla de negocio y usa el repositorio real
        new_record = service.record(
            sensor_id=str(id), 
            value=reading.value, 
            unit=reading.unit
        )
        return new_record
    except ValueError as e:
        if str(e) == "Sensor no encontrado":
            raise HTTPException(status_code=404, detail="Sensor no encontrado")
        # Error 422 si la temperatura está por debajo del cero absoluto
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/readings/{id}", response_model=ReadingOut, status_code=200)
def get_reading(id: int):
    """Obtener una lectura específica"""
    # (Estructura base, pendiente de conectar al servicio en iteraciones futuras)
    return {"id": id, "value": 25.0, "unit": "C"}

@app.patch("/readings/{id}", response_model=ReadingOut, status_code=200)
def update_reading(id: int):
    """Actualizar parcialmente una lectura"""
    # (Estructura base, pendiente de conectar al servicio en iteraciones futuras)
    return {"id": id, "value": 26.0, "unit": "C"}

@app.delete("/readings/{id}", status_code=204)
def delete_reading(id: int):
    """Borrar (desactivar) una lectura"""
    # (Estructura base, pendiente de conectar al servicio en iteraciones futuras)
    return None