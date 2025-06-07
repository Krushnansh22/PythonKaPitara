import cv2

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the trained face recognition model
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_recognizer_model.xml')

# Dictionary to map label to name and enrollment number
label_to_info = {
    0: {"name": "John Doe", "enrollment_no": "12345"},
    # Add more labels and corresponding information here
}

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for face detection and recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Recognize the face
        label, confidence = face_recognizer.predict(gray[y:y + h, x:x + w])

        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display recognized name and enrollment number if available
        if label in label_to_info:
            info = label_to_info[label]
            name = info["name"]
            enrollment_no = info["enrollment_no"]
            text = f'{name} ({enrollment_no})'
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    # Display the frame
    cv2.imshow('Face Recognition', frame)

    # Break the loop on pressing 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
