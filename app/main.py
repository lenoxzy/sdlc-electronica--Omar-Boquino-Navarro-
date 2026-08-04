from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, ForeignKey, DateTime

class Base(DeclarativeBase):
    pass

class SensorModel(Base):
    __tablename__ = "sensors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)

class ReadingModel(Base):
    __tablename__ = "readings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id"), index=True)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String)
    
    # FIX: Agregamos created_at con datetime.now moderno y su índice
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        index=True
    )