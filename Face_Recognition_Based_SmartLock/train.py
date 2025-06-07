# Honeymoon
import os
import cv2
import numpy as np

def get_images_and_labels(data_directory):
    image_paths = [os.path.join(data_directory, f) for f in os.listdir(data_directory) if f.endswith('.jpg')]
    images = []
    labels = []

    for image_path in image_paths:
        # Read the image
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # Extract the label from the image filename
        label = os.path.split(image_path)[-1].split('_')[0]
        # Append the image and label to lists
        images.append(image)
        labels.append(label)

    return images, labels

def prepare_data(images, labels):
    label_dict = {label: idx for idx, label in enumerate(set(labels))}
    labeled_images = []
    labeled_labels = []

    for image, label in zip(images, labels):
        labeled_images.append(image)
        labeled_labels.append(label_dict[label])

    return labeled_images, labeled_labels, label_dict

def train_face_recognizer(data_directory, model_path):
    images, labels = get_images_and_labels(data_directory)
    images, labels, label_dict = prepare_data(images, labels)

    # Convert lists to numpy arrays
    images_np = np.array([np.array(image, 'uint8') for image in images])
    labels_np = np.array(labels)

    # Initialize the face recognizer
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Train the recognizer
    face_recognizer.train(images_np, labels_np)

    # Save the trained model
    face_recognizer.save(model_path)

    return label_dict

if __name__ == "__main__":
    data_directory = 'data'  # Directory containing images
    model_path = 'face_recognizer_model.xml'  # Path to save the trained model

    label_dict = train_face_recognizer(data_directory, model_path)
    print("Training completed. Model saved at:", model_path)
    print("Label dictionary:", label_dict)

import pickle

with open('label_dict.pkl', 'wb') as f:
    pickle.dump(label_dict, f)
print("Done")