import cv2
import os
import streamlit as st


# Function to capture and save face images for training
def capture_training_data(user_name, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    # Counter for images
    img_count = 0

    # Capture images until 'q' is pressed
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Display frame
        cv2.imshow('Capture Training Data', frame)

        # Press 'c' to capture image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Save captured image
            img_name = f"{user_name}_{img_count}.jpg"
            img_path = os.path.join(output_dir, img_name)
            cv2.imwrite(img_path, frame)
            img_count += 1
            st.success(f"Image {img_name} saved.")

        # Press 'q' to quit
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()


# Streamlit UI for capturing training data
def capture_training_data_ui():
    st.title("Capture Training Data")
    user_name = st.text_input("Enter your name:")
    output_dir = st.text_input("Enter output directory:", "training_data")

    if st.button("Start Capture"):
        if user_name:
            capture_training_data(user_name, output_dir)
        else:
            st.error("Please enter a name.")


# Run Streamlit app
if __name__ == "__main__":
    capture_training_data_ui()
