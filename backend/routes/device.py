from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.device import Device
from models.user import User
from schemas.device_schema import DeviceRegister, DeviceResponse
from datetime import date
from sqlalchemy import func
from models.log import Log

router = APIRouter()


@router.post("/device/register", response_model=DeviceResponse)
def register_device(device: DeviceRegister, db: Session = Depends(get_db)):

    # Step 1: Check if user exists
    user = db.query(User).filter(User.id == device.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Step 2: Create device
    new_device = Device(
        device_id=device.device_id,
        user_id=device.user_id,
        location=device.location
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)

    return {
        "status": "device registered",
        "device_id": new_device.device_id
    }

@router.get("/device/{device_id}/daily-calories")
def get_device_daily_calories(device_id: str, db: Session = Depends(get_db)):

    device = db.query(Device).filter(
        Device.device_id == device_id
    ).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    today = date.today()

    total = (
        db.query(func.sum(Log.calculated_calories))
        .filter(
            Log.device_id == device_id,
            func.date(Log.timestamp) == today
        )
        .scalar()
    )

    return {
        "device_id": device_id,
        "date": today,
        "total_calories": round(total or 0, 2)
    }