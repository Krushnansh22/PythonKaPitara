import cv2
import mediapipe as mp
import pyautogui
import time
import threading
import xml.etree.ElementTree as ET

hand_detector = mp.solutions.hands.Hands(min_detection_confidence=0.5)
drawing = mp.solutions.drawing_utils
ptime = 0

screen_width, screen_height = pyautogui.size()

# Load XML file
tree = ET.parse('hand_coordinates.xml')
root = tree.getroot()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduced resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Reduced resolution


def track_hand(frame):
    global ptime
    index_x = index_y = middle_x = middle_y = thumb_x = thumb_y = 0

    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                for finger in root.findall('finger'):
                    finger_id = int(finger.get('id'))
                    cx = int(finger.get('x'))
                    cy = int(finger.get('y'))
                    if id == finger_id:
                        if finger_id == 8:
                            cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 0, 255))
                            index_x = screen_width / frame_width * x
                            index_y = screen_height / frame_height * y
                            pyautogui.moveTo(index_x, index_y)
                        elif finger_id == 4:
                            cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0))
                            thumb_x = screen_width / frame_width * x
                            thumb_y = screen_height / frame_height * y
                            if abs(index_y - thumb_y) < 40:
                                pyautogui.click()
                                pyautogui.sleep(1)
                        elif finger_id == 12:
                            cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0))
                            middle_x = screen_width / frame_width * x
                            middle_y = screen_height / frame_height * y
                            if abs(middle_y - index_y) < 30:
                                pyautogui.rightClick()
                                pyautogui.sleep(1)
                        elif finger_id == 20:
                            pinky_x = screen_width / frame_width * x
                            pinky_y = screen_height / frame_height * y
                            if abs(thumb_x - pinky_x) < 50:
                                pyautogui.press('volumeup')
                        elif finger_id == 16:
                            ring_x = screen_width / frame_width * x
                            ring_y = screen_height / frame_height * y
                        elif finger_id == 13:
                            ring_end_x = screen_width / frame_width * x
                            ring_end_y = screen_height / frame_height * y
                            if abs(thumb_x - ring_end_x) < 50:
                                pyautogui.press('volumedown')


def render_frame():
    global ptime
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        frame = cv2.flip(frame, 1)
        track_hand(frame)
        cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


render_thread = threading.Thread(target=render_frame)
render_thread.daemon = True
render_thread.start()

render_thread.join()
cap.release()
cv2.destroyAllWindows()
