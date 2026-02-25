Endpoints:
POST /device/register
POST /device/weight
POST /device/predict
GET /user/{user_id}/logs

JSON formats:
POST /device/weight
{
  "device_id": "device_01",
  "weight": 150.5,
  "unit": "grams",
  "timestamp": "ISO format"
}