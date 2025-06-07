import cv2
import cvzone

image = cv2.imread('../Faces/Bhushan.3.jpg')
blu=cv2.GaussianBlur(image,(5,5),100)
stack=cvzone.stackImages([image,blu],2,1)
cv2.imshow("Hello",stack)
cv2.waitKey(0)
cv2.destroyAllWindows()