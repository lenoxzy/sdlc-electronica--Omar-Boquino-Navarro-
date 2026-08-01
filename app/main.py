from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import select

# Importamos nuestra configuración de DB y los Modelos ORM
from app.db import SessionLocal, engine, Base
from app.models.models  import Sensor, Reading

# Le decimos a SQLAlchemy que cree las tablas en SQLite al arrancar el servidor
# (Si ya existen, simplemente las ignora)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SensorHub API", version="0.1.0")

# --- DEPENDENCIAS ---
def get_db():
    db = SessionLocal()
    try:
        yield db  # Entrega la sesión al endpoint
    finally:
        db.close()  # Se asegura de cerrar la conexión al terminar

# --- ESQUEMAS PYDANTIC (Para validar la entrada/salida) ---
class SensorReadingIn(BaseModel):
    sensor_name: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"

class SensorReadingOut(BaseModel):
    id: int
    value: float
    unit: str

# --- ENDPOINTS ---
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "db": "connected"}

@app.post("/readings", response_model=SensorReadingOut, status_code=201)
def create_reading(reading: SensorReadingIn, db: Session = Depends(get_db)):
    # 1. Buscamos si el sensor ya existe en la base de datos por su nombre
    stmt = select(Sensor).where(Sensor.name == reading.sensor_name)
    sensor_db = db.scalar(stmt)
    
    # 2. Si el sensor no existe, lo creamos sobre la marcha
    if not sensor_db:
        sensor_db = Sensor(name=reading.sensor_name, location="Desconocida")
        db.add(sensor_db)
        db.commit()
        db.refresh(sensor_db) # Actualiza el objeto con su nuevo ID
        
    # 3. Creamos la nueva lectura asociándola al ID del sensor
    new_reading = Reading(
        value=reading.value,
        unit=reading.unit,
        sensor_id=sensor_db.id
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    
    # Devolvemos el objeto, y Pydantic lo convertirá a JSON según SensorReadingOut
    return new_reading