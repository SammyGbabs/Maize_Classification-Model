from fastapi import APIRouter, File, UploadFile
from io import BytesIO
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

# Router initialization
router = APIRouter()

# Load the model
MODEL = load_model("../models/model_densenet.h5")
CLASS_NAMES = ["Blight", "Common_Rust", "Gray_Leaf_Spot", "Healthy"]

def make_prediction(image):
    # Preprocess the image
    image = image.resize((256, 256))
    image_array = np.array(image) / 255.0
    image_batch = np.expand_dims(image_array, axis=0)

    # Make predictions
    predictions = MODEL.predict(image_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    return {"class": predicted_class, "confidence": float(confidence)}

@router.post("/")
async def predict(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        image = Image.open(BytesIO(file_content)).convert("RGB")
        result = make_prediction(image)
        return {"prediction": result}
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"error": "An internal error occurred."}
