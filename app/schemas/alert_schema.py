from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    reading_id: int
    value: float
    threshold: float
    message: str
    status: str
    created_at: datetime


class AlertStatusUpdate(BaseModel):
    status: Literal["open", "acknowledged", "resolved"]