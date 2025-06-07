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

# Load XML file if it exists, or create a new XML structure
try:
    tree = ET.parse('hand_coordinates.xml')
    root = tree.getroot()
except FileNotFoundError:
    root = ET.Element("hand_coordinates")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduced resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Reduced resolution

action = input("Enter the action label (e.g., click, right_click, volume_up): ")


def track_hand(frame):
    global ptime

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
                # Store the coordinates if the action key is pressed
                if cv2.waitKey(1) & 0xFF == ord('s'):
                    finger_element = ET.SubElement(root, action)
                    finger_element.set("x", str(x))
                    finger_element.set("y", str(y))
                    tree = ET.ElementTree(root)
                    tree.write("hand_coordinates.xml")
                # Your existing code for hand actions goes here...


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
