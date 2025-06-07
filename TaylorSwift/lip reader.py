# pip install opencv-python-headless dlib numpy tensorflow

import cv2

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, LSTM, TimeDistributed

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
cap = cv2.VideoCapture(0)  # 0 is the default camera

def get_lip_coordinates(shape):
    coords = np.array([[shape.part(i).x, shape.part(i).y] for i in range(48, 68)])
    return coords

def preprocess_frame(frame, lip_coords):
    x, y, w, h = cv2.boundingRect(np.array([lip_coords]))
    lips = frame[y:y+h, x:x+w]
    lips = cv2.resize(lips, (50, 50))
    lips = lips / 255.0  # normalize to [0,1]
    return lips

def build_model():
    model = Sequential([
        TimeDistributed(Conv2D(32, (3, 3), activation='relu'), input_shape=(None, 50, 50, 3)),
        TimeDistributed(MaxPooling2D((2, 2))),
        TimeDistributed(Conv2D(64, (3, 3), activation='relu')),
        TimeDistributed(MaxPooling2D((2, 2))),
        TimeDistributed(Flatten()),
        LSTM(128, return_sequences=True),
        LSTM(128),
        Dense(10, activation='softmax')  # Assume 10 classes for demonstration
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = build_model()


sequence = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        lip_coords = get_lip_coordinates(shape)

        for (x, y) in lip_coords:
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        lips = preprocess_frame(frame, lip_coords)
        sequence.append(lips)

        if len(sequence) == 20:  # Example sequence length
            sequence = np.expand_dims(sequence, axis=0)
            preds = model.predict(sequence)
            print(preds)  # Placeholder for actual speech prediction
            sequence = []

    cv2.imshow('Lip Reading', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
