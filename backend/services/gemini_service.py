from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def identify_food(image_path: str):

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            {
                "role": "user",
                "parts": [
                    {
                        "text":
                        "Identify the single food item in this image. "
                        "Return ONLY the food name in lowercase."
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_bytes
                        }
                    }
                ]
            }
        ]
    )

    return response.text.strip().lower()