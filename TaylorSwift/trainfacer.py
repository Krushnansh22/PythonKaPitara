import cv2
import os
import numpy as np

# Create LBPH Face Recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

face_img = []
label = []

for filename in os.listdir('../Faces'):
    path = os.path.join('../Faces', filename)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # Assuming filename is in the format 'label.anything.jpg'
    label_id = int(filename.split('.')[0])  # Extract label as integer
    face_img.append(img)
    label.append(label_id)

# Train the face recognizer
face_recognizer.train(face_img, np.array(label))

# Save the trained model
model_file = 'face_rec_model.xml'
try:
    face_recognizer.save(model_file)
    print(f"Model saved successfully as '{model_file}'")
except cv2.error as e:
    print(f"Error saving model: {e}")
