def calculate_calories(calories_per_100g: float, weight: float) -> float:
    """
    Calculate calories based on weight and calories per 100g.
    """
    return (calories_per_100g * weight) / 100