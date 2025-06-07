import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import cv2
import numpy as np

# Define the autoencoder model
class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, stride=2, padding=1),  # [B, 16, 64, 64]
            nn.ReLU(True),
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),  # [B, 32, 32, 32]
            nn.ReLU(True),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),  # [B, 64, 16, 16]
            nn.ReLU(True),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1), # [B, 128, 8, 8]
            nn.ReLU(True)
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),  # [B, 64, 16, 16]
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1),   # [B, 32, 32, 32]
            nn.ReLU(True),
            nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, output_padding=1),   # [B, 16, 64, 64]
            nn.ReLU(True),
            nn.ConvTranspose2d(16, 1, kernel_size=3, stride=2, padding=1, output_padding=1),    # [B, 1, 128, 128]
            nn.Sigmoid()  # Normalize output to [0,1]
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

# Hyperparameters
learning_rate = 1e-3
num_epochs = 1  # For live training, reduce to a reasonable number
frame_size = (128, 128)  # Resize frame to 128x128
threshold = 0.05  # Reconstruction error threshold for anomaly detection

# Initialize the model, loss function, and optimizer
model = Autoencoder().cuda()
criterion = nn.MSELoss()  # Mean Squared Error for reconstruction
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Video Capture
cap = cv2.VideoCapture(0)  # 0 for default camera

def preprocess_frame(frame):
    """Preprocess the frame: resize, convert to grayscale, and normalize."""
    frame = cv2.resize(frame, frame_size)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = frame / 255.0  # Normalize to [0,1]
    frame = torch.tensor(frame, dtype=torch.float32).unsqueeze(0).unsqueeze(0).cuda()  # [1, 1, H, W]
    return frame

def train_on_frame(frame):
    """Train the autoencoder on the current frame."""
    model.train()
    output = model(frame)
    loss = criterion(output, frame)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss.item()

def detect_anomaly(frame):
    """Detect anomalies by computing the reconstruction error."""
    model.eval()
    with torch.no_grad():
        output = model(frame)
        error = F.mse_loss(output, frame, reduction='mean').item()  # Reconstruction error
    return error

# Training loop on live video feed
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    frame_tensor = preprocess_frame(frame)

    # Train the model on the frame
    loss = train_on_frame(frame_tensor)

    # Detect anomaly
    reconstruction_error = detect_anomaly(frame_tensor)
    is_anomaly = reconstruction_error > threshold

    # Display the results
    display_frame = cv2.putText(
        frame,
        f"Anomaly: {'Yes' if is_anomaly else 'No'} | Error: {reconstruction_error:.4f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if not is_anomaly else (0, 0, 255),
        2
    )

    cv2.imshow('Anomaly Detection', display_frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
