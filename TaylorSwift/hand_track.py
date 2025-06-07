import cv2
import cvzone
import htm
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
import autopy

wcam,hcam = 1000, 1000
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
ptime = 0
detector = HandDetector(detectionCon=0.0, maxHands=1)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findHands(img)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Virtual Touchpad", img)
    cv2.waitKey(1)
