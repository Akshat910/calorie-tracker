from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os

from database import get_db
from models.device import Device
from models.food import Food
from models.log import Log
from services.calorie_service import calculate_calories
from schemas.predict_schema import PredictionResponse
from services.gemini_service import identify_food

router = APIRouter()

# Folder to temporarily store uploaded images
UPLOAD_DIR = "temp_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/device/predict", response_model=PredictionResponse)
async def predict(
    device_id: str,
    weight: float,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # ---------------------------------------------------
    # 1. CHECK DEVICE EXISTS
    # ---------------------------------------------------
    device = db.query(Device).filter(
        Device.device_id == device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not registered"
        )

    # ---------------------------------------------------
    # 2. SAVE IMAGE TEMPORARILY
    # ---------------------------------------------------
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------------------------------------------------
    # 3. GEMINI FOOD IDENTIFICATION
    # ---------------------------------------------------
    predicted_food = identify_food(file_path)
    print("Gemini Prediction:", predicted_food)

    # ---------------------------------------------------
    # 4. FIND FOOD IN DATABASE
    # ---------------------------------------------------
    food = (
        db.query(Food)
        .filter(Food.food_name.ilike(f"%{predicted_food}%"))
        .first()
    )

    if not food:
        os.remove(file_path)
        raise HTTPException(
            status_code=404,
            detail=f"Food '{predicted_food}' not found in database"
        )

    # ---------------------------------------------------
    # 5. CALCULATE CALORIES
    # ---------------------------------------------------
    calories = calculate_calories(
        food.calories_per_100g,
        weight
    )

    # ---------------------------------------------------
    # 6. STORE LOG ENTRY
    # ---------------------------------------------------
    log = Log(
        user_id=device.user_id,
        device_id=device.device_id,
        food_id=food.id,
        weight=weight,
        calculated_calories=calories,
        confidence=0.95
    )

    db.add(log)
    db.commit()

    # ---------------------------------------------------
    # 7. DELETE TEMP IMAGE
    # ---------------------------------------------------
    os.remove(file_path)

    # ---------------------------------------------------
    # 8. RETURN RESPONSE
    # ---------------------------------------------------
    return {
        "food_name": food.food_name,
        "confidence": 0.95,
        "calculated_calories": round(calories, 2)
    }