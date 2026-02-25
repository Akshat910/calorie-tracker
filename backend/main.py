from fastapi import FastAPI
from database import engine, Base

from models import user, device, food, log
from routes import device as device_routes
from routes import predict as predict_routes
from routes import user as user_routes

app = FastAPI(title="IoT Calorie Tracker API")

Base.metadata.create_all(bind=engine)

app.include_router(device_routes.router)
app.include_router(predict_routes.router)
app.include_router(user_routes.router)


@app.get("/")
def root():
    return {"message": "Calorie Tracker API Running"}