
from pathlib import Path
import numpy as np
import tensorflow as tf
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "crop_disease_mobilenetv2.keras"
CLASS_PATH = PROJECT_ROOT / "models" / "class_names.txt"
IMAGE_SIZE = (224, 224)


def load_model_and_classes():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    if not CLASS_PATH.exists():
        raise FileNotFoundError(
            f"Class names file not found: {CLASS_PATH}"
        )

    model = tf.keras.models.load_model(MODEL_PATH)

    with open(CLASS_PATH, "r", encoding="utf-8") as file:
        class_names = file.read().splitlines()

    if model.input_shape != (None, *IMAGE_SIZE, 3):
        raise ValueError(
            f"Expected model input shape (None, {IMAGE_SIZE[0]}, "
            f"{IMAGE_SIZE[1]}, 3), got {model.input_shape}."
        )

    if (not class_names or len(class_names) != model.output_shape[-1]
            or len(class_names) != len(set(class_names))):
        raise ValueError(
            "Class names must be unique and match the model output count."
        )

    return model, class_names


def predict_disease(image, model, class_names):

    if not isinstance(image, Image.Image):
        raise TypeError("Prediction input must be a PIL image.")

    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)

    image_array = tf.keras.utils.img_to_array(image)

    image_array = np.expand_dims(image_array, axis=0)

    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array
    )

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]

    if predictions.ndim != 1 or len(predictions) != len(class_names):
        raise ValueError(
            "Model predictions do not match the provided class names."
        )
    if not np.all(np.isfinite(predictions)):
        raise ValueError("The model returned non-finite prediction scores.")

    predicted_index = int(np.argmax(predictions))

    return {
        "disease": class_names[predicted_index],
        "confidence": float(predictions[predicted_index]) * 100,
        "probabilities": predictions
    }
