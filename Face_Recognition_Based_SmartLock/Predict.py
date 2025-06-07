# Climax

import cv2
import pickle
import time
import AddToExcel


# Flag to check current status

def load_model(model_path):
    # Load the trained face recognizer model
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read(model_path)
    return face_recognizer


def load_label_dict(label_dict_path):
    # Load the label dictionary from a file
    with open(label_dict_path, 'rb') as f:
        label_dict = pickle.load(f)
    return label_dict


def predict_faces(face_recognizer, label_dict, threshold=80):
    global locked_status, current_status
    cap = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    reverse_label_dict = {v: k for k, v in label_dict.items()}

    # Variables to control text display
    display_text = ""
    text_start_time = 0
    display_duration = 2  # Display text for 2 seconds

    while True:
        _, img = cap.read()
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(grey, 1.1, 4)
        cv2.putText(img, "L : Lock/Unlock", (20, 450), 1, 2, (0, 0, 255), 2)

        for (x, y, w, h) in faces:
            face = grey[y:y + h, x:x + w]
            label_id, confidence = face_recognizer.predict(face)

            cv2.putText(img, f"{current_status}", (430, 50), 1, 2, (100, 100, 0), 3)

            if confidence > threshold:
                label = "unknown"
            else:
                label = reverse_label_dict[label_id]

            if locked_status:
                if cv2.waitKey(1) == ord('l'):
                    if label == "unknown":
                        display_text = "Unauthorised Personnel"
                        text_start_time = time.time()
                        # Record Unauthorised access attempts
                        AddToExcel.unauthorized_unlock('unauthaurised.xlsx', img)
                    else:
                        locked_status = not locked_status
                        current_status = "Unlocked"
            elif not locked_status:
                if cv2.waitKey(1) == ord('l'):
                    current_status = "Locked"
                    locked_status = not locked_status

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Check if text should be displayed
        if display_text and (time.time() - text_start_time < display_duration):
            cv2.putText(img, display_text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow('Face Recognition', img)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    locked_status = True
    current_status = "Locked"
    face_recognizer = load_model('face_recognizer_model.xml')
    label_dict = load_label_dict('label_dict.pkl')

    predict_faces(face_recognizer, label_dict)
