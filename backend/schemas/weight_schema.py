from pydantic import BaseModel
from datetime import datetime


class WeightData(BaseModel):
    device_id: str
    weight: float
    unit: str
    timestamp: datetime


class WeightResponse(BaseModel):
    status: str
    device_id: str
    recorded_weight: float