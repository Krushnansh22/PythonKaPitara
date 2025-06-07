import cv2
import os
import numpy as np


def train_face_recognizer():
    # Load pre-trained face recognition model
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load saved face images for training
    face_images = []
    labels = []
    names = []
    enrollment_nos = []

    # Define the directory containing face images
    faces_directory = 'faces'

    # Check if the faces directory exists
    if not os.path.exists(faces_directory):
        print(f"Error: Directory '{faces_directory}' not found.")
        return

    try:
        for filename in os.listdir(faces_directory):
            img_path = os.path.join(faces_directory, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"Error loading image: {filename}")
                continue

            # Extract name and enrollment no from filename
            parts = filename.split('_')
            user_id = int(parts[1])
            name = parts[2]
            names.append(name)
            enrollment_no = parts[3].split('.')[0]
            enrollment_nos.append(enrollment_no)

            face_images.append(img)
            labels.append(user_id)

        # Train the face recognition model
        face_recognizer.train(face_images, np.array(labels))

        # Save the trained model
        face_recognizer.save('face_recognizer_model.xml')

        # Save names and enrollment nos to a file
        with open('names_enrollment.txt', 'w') as file:
            for i in range(len(names)):
                file.write(f"Name: {names[i]}, Enrollment No: {enrollment_nos[i]}\n")

        print('Face recognition model trained and saved.')

    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function to train the face recognition model
train_face_recognizer()
