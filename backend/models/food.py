from sqlalchemy import Column, Integer, String, Float
from database import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)

    food_name = Column(String, unique=True, nullable=False)

    calories_per_100g = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)