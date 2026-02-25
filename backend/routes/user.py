from fastapi import APIRouter
from schemas.user_schema import UserCreate, UserResponse

router = APIRouter()


@router.post("/user/create", response_model=UserResponse)
def create_user(user: UserCreate):
    return {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "goal_calories": user.goal_calories
    }


@router.get("/user/{user_id}/logs")
def get_user_logs(user_id: int):
    return {
        "user_id": user_id,
        "logs": []
    }