from flask import Flask, request, render_template, jsonify
import numpy as np
import cv2
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load your trained model
MODEL_PATH = "deepfake_cnn_model(train only).h5"
model = load_model(MODEL_PATH)

# Binary classification
class_names = ["Real", "Fake"]

# Route: Home page
@app.route('/')
def home():
    return render_template('index.html')

# Route: Prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    # Read image file as numpy array
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    # Preprocess for model
    img = cv2.resize(img, (128,128))
    img = img / 255.0
    img = img.reshape(1, 128,128,3)

    # Predict
    prediction = model.predict(img)
    pred_index = np.argmax(prediction)
    confidence = float(np.max(prediction)) * 100
    pred_label = class_names[pred_index]

    return jsonify({"prediction": pred_label, "confidence": f"{confidence:.2f}%"})

if __name__ == '__main__':
    app.run(debug=True)
