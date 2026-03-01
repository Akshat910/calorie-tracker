from pydantic import BaseModel


class PredictionResponse(BaseModel):
    food_name: str
    confidence: float
    calculated_calories: float