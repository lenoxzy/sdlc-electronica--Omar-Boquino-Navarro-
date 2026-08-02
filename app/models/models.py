from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String, index=True)
    type = Column(String, nullable=False)      # <-- NUEVA COLUMNA
    location = Column(String, nullable=True)   # <-- NUEVA COLUMNA

    # Relación con las lecturas (Un sensor tiene muchas lecturas)
    readings = relationship("Reading", back_populates="sensor", cascade="all, ")

class Reading(Base):
    __tablename__ = "reading"

    id = Column(Integer, primary_key=True,index=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)

    # Relación inversa (Una lectura pertenece a un sensor)
    sensor = relationship("Sensor", back_populates="readings")