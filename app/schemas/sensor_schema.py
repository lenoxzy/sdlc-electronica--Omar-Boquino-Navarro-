
from pydantic import BaseModel, ConfigDict


class SensorCreate(BaseModel):
    name: str
    type: str
    location: str | None = None

class SensorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Pydantic V2

    id: int
    name: str
    type: str
    location: str | None = None