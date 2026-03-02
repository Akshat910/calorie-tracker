from google import genai
from dotenv import load_dotenv
import os
import json

from database import SessionLocal
from models.food import Food

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_food_nutrition(food_name: str):

    prompt = f"""
    Provide nutritional values per 100 grams of {food_name}.

    Return STRICT JSON:

    {{
        "calories": float,
        "protein": float,
        "carbs": float,
        "fats": float
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "")

    data = json.loads(text)

    db = SessionLocal()

    new_food = Food(
        food_name=food_name,
        calories_per_100g=data["calories"],
        protein=data["protein"],
        carbs=data["carbs"],
        fats=data["fats"]
    )

    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    db.close()

    return new_food