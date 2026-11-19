
def format_disease_name(class_name):
    parts = class_name.split("___")
    crop = parts[0].replace("_", " ")
    condition = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
    condition = condition.strip()

    if condition.lower() == "healthy":
        return crop, "Healthy"

    return crop, condition


def get_disease_info(class_name):
    crop, disease = format_disease_name(class_name)

    if disease.lower() == "healthy":
        return {
            "crop": crop,
            "disease": "Healthy",
            "status": "No disease detected by the model",
            "description": (
                "The model classified this image as belonging "
                "to the healthy category."
            ),
            "management": [
                "Continue regular crop monitoring.",
                "Maintain suitable irrigation and nutrition.",
                "Inspect leaves regularly for changes.",
            ],
        }

    return {
        "crop": crop,
        "disease": disease,
        "status": "Potential disease detected",
        "description": (
            f"The model identified visual patterns associated "
            f"with {disease} in {crop}. This is an AI prediction "
            "and should be checked against field symptoms."
        ),
        "management": [
            "Inspect other leaves and plants for similar symptoms.",
            "Remove heavily affected plant material where appropriate "
            "and follow local agricultural guidance.",
            "Avoid overhead watering if leaf wetness is contributing "
            "to disease conditions.",
            "Consult a local agricultural expert before applying "
            "any crop treatment.",
        ],
    }
