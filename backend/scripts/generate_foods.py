import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google import genai
from google.genai import errors as genai_errors
from dotenv import load_dotenv
import json
import time

from database import SessionLocal
from models.food import Food

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

foods = [
    # Fruits
    "apple","banana","orange","mango","pineapple","grapes",
    "watermelon","papaya","pomegranate","guava",

    # Vegetables
    "potato","tomato","carrot","cabbage","broccoli",
    "spinach","onion","peas","corn","capsicum",

    # Indian Staples
    "rice","brown rice","roti","naan","paratha",
    "dal","sambar","idli","dosa","upma",

    # Protein Foods
    "egg","boiled egg","chicken breast","fried chicken",
    "fish curry","paneer","tofu","lentils","chickpeas","rajma",

    # Fast Foods
    "pizza","burger","sandwich","hotdog","french fries",
    "noodles","pasta","fried rice","biryani","shawarma",

    # Dairy
    "milk","curd","cheese","butter","ice cream",

    # Snacks & Others
    "cake","biscuits","chocolate","chips","popcorn"
]

def generate_nutrition(food_name):

    prompt = f"""
    Give nutritional values per 100 grams for {food_name}.
    Return STRICT JSON format:

    {{
      "calories": number,
      "protein": number,
      "carbs": number,
      "fats": number
    }}
    """

    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            break
        except genai_errors.ClientError as e:
            if e.status_code == 429:
                wait = 60 * (attempt + 1)
                print(f"  Rate limited. Waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                raise
    else:
        raise RuntimeError(f"Failed to generate nutrition for {food_name} after retries")

    text = response.text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    return json.loads(text)


def main():

    db = SessionLocal()

    for food in foods:
        existing = db.query(Food).filter(
            Food.food_name == food
        ).first()
        
        if existing:
            print(f"Skipping {food}")
            continue
        
        print("Generating:", food)
        
        data = generate_nutrition(food)
        
        new_food = Food(
            food_name=food,
            calories_per_100g=data["calories"],
            protein=data["protein"],
            carbs=data["carbs"],
            fats=data["fats"]
        )
        db.add(new_food)
    db.commit()
    print("✅ Food database populated")


if __name__ == "__main__":
    main()