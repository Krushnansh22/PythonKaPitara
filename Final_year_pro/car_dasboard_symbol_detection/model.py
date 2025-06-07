import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import matplotlib.pyplot as plt

# Load the dataset
file_path = '../../DLP]/Symbols.csv'  # Ensure this path is correct
data = pd.read_csv(file_path)

# Parameters
img_size = (128, 128)  # Resize images to 128x128

# Preprocessing function to load and process images
def preprocess_image(image_path):
    image = load_img(image_path, target_size=img_size)
    image = img_to_array(image) / 255.0  # Normalize image
    return image

# Load images and labels
images = np.array([preprocess_image(image_path) for image_path in data['image_path']])
labels = to_categorical(data['label'], num_classes=len(data['label'].unique()))  # One-hot encoding labels

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Build the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(data['label'].unique()), activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Function to classify a symbol from an image path
def classify_symbol(image_path):
    image = preprocess_image(image_path)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    prediction = model.predict(image)
    predicted_label = np.argmax(prediction)
    return predicted_label, data.loc[data['label'] == predicted_label, 'solution'].values[0], image[0]

# Test the model with a user-provided image
user_image_path = input("Enter the image path: ")
label, solution, predicted_image = classify_symbol(user_image_path)

# Display the predicted label, solution, and the image
print(f"Predicted Label: {label}, Solution: {solution}")

# Show the predicted image
plt.imshow(predicted_image)
plt.axis('off')  # Hide the axes
plt.title(f'Predicted Label: {label}, Solution: {solution}')
plt.show()
