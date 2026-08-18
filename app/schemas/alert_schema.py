from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    reading_id: int
    value: float
    threshold: float
    message: str
    created_at: datetime