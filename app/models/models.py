from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base 

class Sensor(Base):
    __tablename__ = "sensor"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    location: Mapped[Optional[str]]
    
    readings: Mapped[List["Reading"]] = relationship(
        back_populates="sensor", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Sensor(id={self.id!r}, name={self.name!r}, location={self.location!r})"

class Reading(Base):
    __tablename__ = "reading"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float]
    unit: Mapped[str] = mapped_column(String(10))
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"))
    
    sensor: Mapped["Sensor"] = relationship(back_populates="readings")

    def __repr__(self) -> str:
        return f"Reading(id={self.id!r}, value={self.value!r}, unit={self.unit!r})"