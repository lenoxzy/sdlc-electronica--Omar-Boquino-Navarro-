
from pydantic import BaseModel, ConfigDict


class SensorCreate(BaseModel):
    name: str
    type: str
    location: str | None = None
    alert_threshold: float | None = None


class SensorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    location: str | None = None
    alert_threshold: float | None = None
    is_active: bool

    