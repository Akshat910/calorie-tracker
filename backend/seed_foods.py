import csv
from database import SessionLocal
from models.food import Food

CSV_FILE_PATH = "C:\\Users\\aksha\\Desktop\\IoT Project\\calorie-tracker\\backend\\nutrients_csvfile.csv"


def seed_foods():
    db = SessionLocal()
    seen_names = set()

    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:

            food_name = row.get("Food")
            grams = row.get("Grams")
            calories = row.get("Calories")
            protein = row.get("Protein")
            carbs = row.get("Carbs")
            fats = row.get("Fat")

            if not food_name or not calories or not grams:
                continue

            try:
                grams = float(grams)
                calories = float(calories)

                if grams == 0:
                    continue

                normalized_name = food_name.lower().strip()

                if normalized_name in seen_names:
                    continue

                #Convert to per 100g
                calories_per_100g = (calories / grams) * 100

                existing_food = db.query(Food).filter(
                    Food.food_name == normalized_name
                ).first()

                if existing_food:
                    seen_names.add(normalized_name)
                    continue

                new_food = Food(
                    food_name=normalized_name,
                    calories_per_100g=round(calories_per_100g, 2),
                    protein=float(protein) if protein else 0,
                    carbs=float(carbs) if carbs else 0,
                    fats=float(fats) if fats else 0
                )

                db.add(new_food)
                seen_names.add(normalized_name)

            except ValueError:
                continue

        db.commit()

    db.close()
    print("Food data seeded successfully.")


if __name__ == "__main__":
    seed_foods()