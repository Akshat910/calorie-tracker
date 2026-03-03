import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google import genai
from dotenv import load_dotenv
import json

from database import SessionLocal
from models.food import Food

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

foods = [
    "apple","banana","orange","mango","pineapple","grapes",
    "watermelon","papaya","pomegranate","guava",
    "potato","tomato","carrot","cabbage","broccoli",
    "spinach","onion","peas","corn","capsicum",
    "rice","brown rice","roti","naan","paratha",
    "dal","sambar","idli","dosa","upma",
    "egg","boiled egg","chicken breast","fried chicken",
    "fish curry","paneer","tofu","lentils","chickpeas","rajma",
    "pizza","burger","sandwich","hotdog","french fries",
    "noodles","pasta","fried rice","biryani","shawarma",
    "milk","curd","cheese","butter","ice cream",
    "cake","biscuits","chocolate","chips","popcorn"
]


def generate_bulk_nutrition(food_list):

    prompt = f"""
    For each of the following foods, provide nutrition per 100 grams.

    Return STRICT JSON in this format:

    {{
      "apple": {{"calories": float, "protein": float, "carbs": float, "fats": float}},
      "banana": {{"calories": float, "protein": float, "carbs": float, "fats": float}},
      ...
    }}

    Foods:
    {", ".join(food_list)}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "")

    return json.loads(text)


def main():

    print("Generating nutrition data in ONE API request...")

    data = generate_bulk_nutrition(foods)

    db = SessionLocal()

    for food_name, values in data.items():

        existing = db.query(Food).filter(
            Food.food_name == food_name
        ).first()

        if existing:
            print(f"Skipping {food_name}")
            continue

        new_food = Food(
            food_name=food_name,
            calories_per_100g=values["calories"],
            protein=values["protein"],
            carbs=values["carbs"],
            fats=values["fats"]
        )

        db.add(new_food)

    db.commit()
    db.close()

    print("✅ Database populated successfully")


if __name__ == "__main__":
    main()