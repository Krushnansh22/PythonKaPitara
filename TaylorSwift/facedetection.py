import cv2
import numpy as np
import os

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)


def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces_this = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces_this:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (255, 0, 0), 4)
    return faces_this


while True:

    result, video_frame = video_capture.read()
    if result is False:
        break

    faces_this = detect_bounding_box(video_frame)
    cv2.imshow("Krupaya Apna Shri-Mukh Dikhaye", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
