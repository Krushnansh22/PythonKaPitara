import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize Mediapipe Drawing
mp_drawing = mp.solutions.drawing_utils


# Function to calculate the angle between two points
def calculate_angle(a, b):
    angle = np.arctan2(b[1] - a[1], b[0] - a[0])
    return np.degrees(angle)


# Function to calculate steering angle based on hand positions
def calculate_steering_angle(landmarks):
    if len(landmarks) >= 2:
        # Get coordinates of the landmarks of interest (index finger tip of both hands)
        left_hand = landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        right_hand = landmarks[1].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Convert normalized coordinates to pixel coordinates
        left_hand = (int(left_hand.x * width), int(left_hand.y * height))
        right_hand = (int(right_hand.x * width), int(right_hand.y * height))

        # Calculate the angle between the hands
        angle = calculate_angle(left_hand, right_hand)
        return angle
    return 0


# Function to control the game based on the steering angle
def control_game(angle, forward):
    if forward:
        pyautogui.keyDown('w')
    else:
        pyautogui.keyUp('w')

    if angle < -1:  # Turn left
        pyautogui.keyDown('a')
        pyautogui.keyUp('d')
    elif angle > 1:  # Turn right
        pyautogui.keyDown('d')
        pyautogui.keyUp('a')
    else:  # Go straight
        pyautogui.keyUp('a')
        pyautogui.keyUp('d')


# Start capturing video from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Convert the BGR image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the image and detect hands
    results = hands.process(image)

    # Draw hand landmarks
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Calculate the steering angle
        steering_angle = calculate_steering_angle(results.multi_hand_landmarks)

        # Check if hands are in forward position (e.g., both hands in upper half of the frame)
        forward = all(hand.landmark[mp_hands.HandLandmark.WRIST].y < 0.5 for hand in results.multi_hand_landmarks)

        # Control the game based on the steering angle
        control_game(steering_angle, forward)

        # Display the steering angle on the image
        cv2.putText(image, f'Steering Angle: {steering_angle:.2f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(image, f'Forward: {forward}', (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Steering Control', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

# Release keys when exiting
pyautogui.keyUp('w')
pyautogui.keyUp('a')
pyautogui.keyUp('d')
