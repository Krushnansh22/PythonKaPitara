import cv2

def process_frame(frame, thermal):
    if thermal:
        normalized_img = cv2.normalize(frame, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        return cv2.applyColorMap(normalized_img, cv2.COLORMAP_HOT)
    return frame

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

thermal_mode = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    frame = process_frame(frame, thermal_mode)
    cv2.imshow('Video Feed', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('t'):
        thermal_mode = not thermal_mode

cap.release()
cv2.destroyAllWindows()
