from pydantic import BaseModel
from datetime import datetime


class PredictionRequest(BaseModel):
    device_id: str
    weight: float


class PredictionResponse(BaseModel):
    food_name: str
    confidence: float
    calculated_calories: float
    timestamp: datetime