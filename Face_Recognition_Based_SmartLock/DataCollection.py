# Muh-dikhai ki rasam
import cv2
import os

cap = cv2.VideoCapture(0)
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
count = 0
name = input("Enter name - ")

while True:
    _, img = cap.read()
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(grey, 1.1, 6)  # Adjust scaleFactor and minNeighbors for better results

    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cropped = grey[y:y + h, x:x + w]
        cv2.putText(img, "S : Save", (20, 400), 0, 1.5, (255, 0, 0), 2)
        cv2.putText(img, "Q : Quit", (20, 450), 0, 1.5, (255, 0, 0), 2)
        cv2.imshow("Capture Data", img)

        if cv2.waitKey(1) == ord('s'):
            if not os.path.exists('data'):
                os.makedirs('data')
            image = cv2.resize(cropped, (100, 100))
            file_path = os.path.join('data', f"{name}_{count}.jpg")
            cv2.imwrite(file_path, image)
            print(f"Saved: {file_path}")
            count += 1

        break  # Ensure only one detection at a time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
