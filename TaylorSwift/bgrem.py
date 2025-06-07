import cvzone
import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
# cap.set(cv2.CAP_PROP_FPS,60)
segmentor=SelfiSegmentation()
fps=cvzone.FPS()

imgBg=cv2.imread("../backgrounds/hel.jpg")

listImg = os.listdir("../backgrounds")
print(listImg)

index = 0

imglist = []

for imgPath in listImg:
    img=cv2.imread(f'backgrounds/{imgPath}')
    imglist.append(img)

while True:
    success, img = cap.read()
    imgOut = segmentor.removeBG(img, imglist[index], threshold=0.8)

    imgstacked= cvzone.stackImages([img, imgOut], 2, 1)
    _, imgstacked = fps.update(imgstacked)
    cv2.imshow("Image", imgstacked)
    key = cv2.waitKey(1)
    if key == ord('a'):
        if index > 0:
            index -= 1
    elif key == ord('d'):
        if index < (len(imglist)-1):
            index += 1
    elif key == ord('q'):
        break