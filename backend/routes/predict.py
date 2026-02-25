from fastapi import APIRouter
from datetime import datetime
from schemas.predict_schema import PredictionRequest, PredictionResponse
from services.calorie_service import calculate_calories

router = APIRouter()


@router.post("/device/predict", response_model=PredictionResponse)
def predict_food(request: PredictionRequest):

    # Temporary placeholder value (will come from Food table later)
    calories_per_100g = 130  

    calculated = calculate_calories(calories_per_100g, request.weight)

    return {
        "food_name": "rice",
        "confidence": 0.95,
        "calculated_calories": calculated,
        "timestamp": datetime.utcnow()
    }