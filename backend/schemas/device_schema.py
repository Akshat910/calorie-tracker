from pydantic import BaseModel
from datetime import datetime


class DeviceRegister(BaseModel):
    device_id: str
    user_id: int
    location: str


class DeviceResponse(BaseModel):
    status: str
    device_id: str