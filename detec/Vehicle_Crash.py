import cv2
import torch

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


def detect_vehicle_crash(video_path):
    cap = cv2.VideoCapture(video_path)
    crash_alert_list = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame_rgb)
        detections = results.xyxy[0]

        for *xyxy, conf, cls in detections:
            label = f'{model.names[int(cls)]} {conf:.2f}'
            if model.names[int(cls)] == 'car' or model.names[int(cls)] == 'truck':
                # Logic for crash detection
                crash_alert_list.append(1 if conf > 0.5 else 0)

                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255, 0, 0), 2)
                cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)

        if len(crash_alert_list) > 20 and sum(crash_alert_list[-20:]) > 15:
            print("Crash Detected")
            cv2.putText(frame, "Crash Detected", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            print("Crash Not Detected")
            cv2.putText(frame, "Crash Not Detected", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Vehicle Crash Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_vehicle_crash('vehicle_crash_video.mp4')
