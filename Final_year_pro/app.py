from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load your trained model (make sure to save it beforehand)
model = load_model('symbol_classifier.h5')  # Update with your model path
data = pd.read_csv('Symbols.csv')  # Load your CSV with labels and solutions

img_size = (128, 128)  # Set the image size

# Preprocessing function
def preprocess_image(image_path):
    image = load_img(image_path, target_size=img_size)
    image = img_to_array(image) / 255.0
    return image

@app.route('/solution', methods=['POST'])
def classify():
    image_path = request.json['image_path']
    image = preprocess_image(image_path)
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    predicted_label = np.argmax(prediction)
    solution = data.loc[data['label'] == predicted_label, 'solution'].values[0]
    return jsonify({'label': int(predicted_label), 'solution': solution})

if __name__ == "__main__":
    app.run(debug=True)