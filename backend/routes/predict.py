from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.food import Food
from models.log import Log
from models.device import Device
from schemas.predict_schema import PredictionRequest, PredictionResponse
from services.calorie_service import calculate_calories

router = APIRouter()


@router.post("/device/predict", response_model=PredictionResponse)
def predict_food(request: PredictionRequest, db: Session = Depends(get_db)):

    # 🔹 Step 1: Check if device exists
    device = db.query(Device).filter(Device.device_id == request.device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not registered")

    # 🔹 Step 2: Temporary ML prediction (replace later with real ML)
    predicted_food_name = "rice"

    # 🔹 Step 3: Fetch food from DB
    food = db.query(Food).filter(Food.food_name == predicted_food_name).first()

    if not food:
        raise HTTPException(status_code=404, detail="Food not found in database")

    # 🔹 Step 4: Calculate calories
    calculated = calculate_calories(food.calories_per_100g, request.weight)

    # 🔹 Step 5: Store log entry
    new_log = Log(
        user_id=device.user_id,
        device_id=device.device_id,
        food_id=food.id,
        weight=request.weight,
        calculated_calories=calculated,
        confidence=0.95
    )

    db.add(new_log)
    db.commit()

    return {
        "food_name": food.food_name,
        "confidence": 0.95,
        "calculated_calories": round(calculated, 2),
        "timestamp": datetime.utcnow()
    }