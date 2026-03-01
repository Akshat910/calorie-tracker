FOOD_LABEL_MAPPING = {
    "banana": "banana",
    "pizza": "pizza",
    "cheeseburger": "burger",
    "bakery": "bread",
    "sandwich": "bread",
    "hotdog": "sausage",
    "plate": "rice",
    "dining_table": "rice"
}


def map_prediction(label: str):
    return FOOD_LABEL_MAPPING.get(label.lower())