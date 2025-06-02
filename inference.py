# inference.py

import numpy as np
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# ✅ Local paths (place all files in same directory as app.py)
MODEL_PATH = 'final_model_phase8.h5'
CLASS_INDEX_PATH = 'class_indices.json'
EXPLANATIONS_PATH = 'fault_explanations.json'  # <- updated file

def predict_warning_light(img_path):
    try:
        # Load model and supporting files
        model = load_model(MODEL_PATH)

        with open(CLASS_INDEX_PATH, 'r') as f:
            class_indices = json.load(f)

        with open(EXPLANATIONS_PATH, 'r') as f:
            fault_info = json.load(f)

        # Image preprocessing
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction)
        predicted_label = list(class_indices.keys())[predicted_index]
        confidence = float(prediction[0][predicted_index])
        print("🔍 Predicted Label:", predicted_label)


        # Get explanation data (with fallback)
        explanation = fault_info.get(predicted_label, {
            "title": predicted_label,
            "description": "No additional info available.",
            "severity": "Unknown",
            "recommendation": ["No recommendation available."]
        })

        return {
            "label": predicted_label,
            "confidence": round(confidence * 100, 2),
            "title": explanation["title"],
            "description": explanation["description"],
            "severity": explanation["severity"],
            "recommendation": explanation["recommendation"]
        }

    except Exception as e:
        return {
            "label": "Error",
            "confidence": 0,
            "title": "Error",
            "description": str(e),
            "severity": "Unknown",
            "recommendation": ["Something went wrong. Please check logs."]
        }
