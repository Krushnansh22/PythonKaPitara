import cv2

cap = cv2.VideoCapture(0)
name = input("Enter Name - ")
count = 1
while True:
    ret, frame = cap.read()

    cv2.imshow('Training model....',frame)

    if cv2.waitKey(1) & 0xff == ord('s'):
        cv2.imwrite(f'Faces/{name}.{count}.jpg', frame)
        print(f"Captured {count}")
        count += 1

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()