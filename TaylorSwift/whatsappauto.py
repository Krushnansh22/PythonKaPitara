import pywhatkit as kit
import time
import pyautogui
# Function to send a WhatsApp

def send_whatsapp_message(phone_number, message, interval):
    # Open WhatsApp Web and send the message
    while True:
        try:
            # Send the message
            kit.sendwhatmsg_instantly(phone_number, message, 15, True, 2)
            print(f"Message sent to {phone_number}")
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait for the specified interval before sending the next message
        time.sleep(interval)
        pyautogui.press('enter')

# Define the phone number, message, and interval (in seconds)
phone_number = "+919021263047"  # Replace with the target phone number
message = "Hemlo bhaiya"  # Replace with your custom message
interval = 0.2  # Interval in seconds

# Start sending messages
send_whatsapp_message(phone_number, message, interval)
