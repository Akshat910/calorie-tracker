from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from sqlalchemy import func
from database import get_db
from models.user import User
from models.log import Log
from models.food import Food
from schemas.user_schema import UserCreate, UserResponse

router = APIRouter()


# ---------------------------------------------------
# CREATE USER
# ---------------------------------------------------
@router.post("/user/create", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        name=user.name,
        email=user.email,
        goal_calories=user.goal_calories
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------------------------------------------------
# GET USER FOOD LOG HISTORY
# ---------------------------------------------------
@router.get("/user/{user_id}/logs")
def get_user_logs(user_id: int, db: Session = Depends(get_db)):

    # ✅ Check if user exists
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Join logs with food table
    results = (
        db.query(Log, Food)
        .join(Food, Log.food_id == Food.id)
        .filter(Log.user_id == user_id)
        .all()
    )

    response = []

    for log, food in results:
        response.append({
            "food_name": food.food_name,
            "weight": log.weight,
            "calories": log.calculated_calories,
            "confidence": log.confidence,
            "timestamp": log.timestamp
        })

    return response

@router.get("/user/{user_id}/daily-calories")
def get_daily_calories(user_id: int, db: Session = Depends(get_db)):

    # ✅ Check if user exists
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today()

    total = (
        db.query(func.sum(Log.calculated_calories))
        .filter(
            Log.user_id == user_id,
            func.date(Log.timestamp) == today
        )
        .scalar()
    )

    return {
        "user_id": user_id,
        "date": today,
        "total_calories": round(total or 0, 2)
    }

@router.get("/user/{user_id}/weekly-calories")
def get_weekly_calories(user_id: int, db: Session = Depends(get_db)):

    # ✅ Check user exists
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today()
    seven_days_ago = today - timedelta(days=6)

    results = (
        db.query(
            func.date(Log.timestamp).label("day"),
            func.sum(Log.calculated_calories).label("total")
        )
        .filter(
            Log.user_id == user_id,
            func.date(Log.timestamp) >= seven_days_ago
        )
        .group_by(func.date(Log.timestamp))
        .order_by(func.date(Log.timestamp))
        .all()
    )

    response = []

    for day, total in results:
        response.append({
            "date": str(day),
            "calories": round(total, 2)
        })

    return response