from fastapi import APIRouter
from schemas.device_schema import DeviceRegister, DeviceResponse
from schemas.weight_schema import WeightData, WeightResponse

router = APIRouter()


@router.post("/device/register", response_model=DeviceResponse)
def register_device(device: DeviceRegister):
    return {
        "status": "device registered",
        "device_id": device.device_id
    }


@router.post("/device/weight", response_model=WeightResponse)
def receive_weight(data: WeightData):
    return {
        "status": "weight received",
        "device_id": data.device_id,
        "recorded_weight": data.weight
    }