from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.sql import func
from database import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(String, ForeignKey("devices.device_id"))

    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)

    weight = Column(Float, nullable=False)
    calculated_calories = Column(Float, nullable=False)
    confidence = Column(Float)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())