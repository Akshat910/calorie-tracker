from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    goal_calories: int


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    goal_calories: int