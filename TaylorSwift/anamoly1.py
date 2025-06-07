import torch
import torch.nn as nn
import torch.optim as optim
import cv2
import numpy as np

# Hyperparameters
learning_rate = 1e-4
epochs = 1  # Train for 1 epoch on each frame, continuously update the model
batch_size = 1  # Process frame by frame
image_size = (64, 64)  # Resize frame to 64x64
threshold = 0.01  # Reconstruction error threshold for anomaly detection


# Define Autoencoder model
class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()
        # Encoder
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, 7)
        )
        # Decoder
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 32, 7),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 16, 3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(16, 1, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()  # Output between 0 and 1 (same as normalized input)
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x


# Initialize model, loss function, and optimizer
model = Autoencoder().cuda() if torch.cuda.is_available() else Autoencoder()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)


# Function to preprocess frames (resize, grayscale, normalize)
def preprocess_frame(frame):
    frame = cv2.resize(frame, image_size)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = frame / 255.0  # Normalize to [0, 1]
    frame = np.expand_dims(frame, axis=0)  # Add channel dimension
    frame = np.expand_dims(frame, axis=0)  # Add batch dimension
    return torch.tensor(frame, dtype=torch.float32)


# OpenCV video capture
cap = cv2.VideoCapture(0)  # Capture from webcam

# Training loop for real-time learning and anomaly detection
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    input_frame = preprocess_frame(frame)
    input_frame = input_frame.cuda() if torch.cuda.is_available() else input_frame

    # Forward pass (Autoencoder reconstruction)
    reconstructed_frame = model(input_frame)

    # Compute reconstruction loss
    loss = criterion(reconstructed_frame, input_frame)

    # Backward pass and update model
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Calculate reconstruction error
    error = loss.item()

    # Anomaly detection based on reconstruction error
    if error > threshold:
        anomaly_detected = True
        cv2.putText(frame, "Anomaly Detected!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        anomaly_detected = False

    # Display the frame with anomaly detection result
    cv2.imshow('Real-time Video Feed', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
