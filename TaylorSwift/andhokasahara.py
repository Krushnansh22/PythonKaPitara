import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20

while True:
    success, img = cap.read()
    hands, img =detector.findHands(img)

    if hands:
        hands = hands[0]
        x, y, w ,h = hands['bbox']
        imgCrop = img[(y-offset):(y+h+offset) , (x-offset):(x+w+offset)]
        cv2.imshow("ImageCrop", imgCrop)

    cv2.imshow("Image", img)
    cv2.waitKey(1)