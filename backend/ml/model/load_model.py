from tensorflow.keras.applications import MobileNetV2

model = None


def load_ml_model():
    global model

    if model is None:
        model = MobileNetV2(
            weights="imagenet",
            include_top=True
        )

    return model