import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image

from ml.model.load_model import load_ml_model


def predict_food(image_path: str):

    model = load_ml_model()

    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)

    decoded = decode_predictions(predictions, top=1)[0][0]

    predicted_label = decoded[1]

    return predicted_label

if __name__ == "__main__":
    result = predict_food("test_images/food.jpg")
    print("Prediction:", result)