import cv2

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the trained face recognition model
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_recognizer_model.xml')

# Load names and enrollment nos from the file
names_enrollment = {}
try:
    with open('names_enrollment.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            name = parts[0].split(': ')[1]
            enrollment_no = parts[1].split(': ')[1]
            names_enrollment[int(enrollment_no)] = name
except FileNotFoundError:
    print("Error: 'names_enrollment.txt' not found.")
    exit()
except Exception as e:
    print(f"An error occurred while reading names_enrollment.txt: {e}")
    exit()

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

        # Draw a rectangle around the face and display label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display Name and Enrollment No on the frame
        if label in names_enrollment:
            name = names_enrollment[label]
            cv2.putText(frame, f'Name: {name}', (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(frame, f'Enrollment No: {label}', (x, y + h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0),
                        2)
        else:
            cv2.putText(frame, f'Person {label} (Unknown)', (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0),
                        2)

    # Display the frame
    cv2.imshow('Face Recognition', frame)

    # Break the loop on pressing 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()