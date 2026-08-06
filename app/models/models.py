from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Sensor(Base):
    __tablename__ = "sensor"

    # Sintaxis 2.x usando Mapped y mapped_column
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str | None] = mapped_column(String, nullable=True)

 # Relación con las lecturas (Un sensor tiene muchas lecturas)
    readings: Mapped[list["Reading"]] = relationship(
        "Reading",
        back_populates="sensor",
        cascade="all, delete-orphan"
    )


class Reading(Base):
    __tablename__ = "reading"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"))
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    
    # ✅ FIX: Agregamos la columna created_at con la fecha moderna para los filtros
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        index=True
    )

    # Relación inversa (Una lectura pertenece a un sensor)
    sensor: Mapped["Sensor"] = relationship("Sensor", back_populates="readings")