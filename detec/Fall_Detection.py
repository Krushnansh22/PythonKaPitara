import cv2
import torch

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def detect_fall(video_path):
    cap = cv2.VideoCapture(video_path)
    fall_alert_list = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame_rgb)
        detections = results.xyxy[0]

        for *xyxy, conf, cls in detections:
            label = f'{model.names[int(cls)]} {conf:.2f}'
            if model.names[int(cls)] == 'person':
                # Logic for fall detection based on bbox movement
                if xyxy[3] - xyxy[1] < 100:  # example fall logic based on height
                    fall_alert_list.append(1)
                else:
                    fall_alert_list.append(0)

                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)
                cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)

        if len(fall_alert_list) > 20 and sum(fall_alert_list[-20:]) == 20:
            print("Fall Detected")
            cv2.putText(frame, "Fall Detected", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            print("Fall Not Detected")
            cv2.putText(frame, "Fall Not Detected", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Fall Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_fall('fall_detection_video.mp4')
