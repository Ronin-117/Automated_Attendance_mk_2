import cv2
import os

# Create output folder if it doesn't exist
output_folder = 'captured_frames'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize the webcam (use 0 for the default camera)
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Set the resolution to 3840x2160
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

fourcc= cv2.VideoWriter_fourcc(*'MJPG')
cap.set(cv2.CAP_PROP_FOURCC,fourcc)
cap.set(cv2.CAP_PROP_FORMAT,-1)

# Get the actual resolution after setting
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Resolution set to: {width} x {height}")

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Capture one frame from the camera
ret, frame = cap.read()

# Check if the frame was captured successfully
if ret:

    # Create the output file path
    output_path = os.path.join(output_folder, 'captured_frame_high_res.jpg')

    # Save the frame as a JPG file in its full resolution
    cv2.imwrite(output_path, frame)

    print(f"Frame captured and saved as {output_path}")
    print(f"Frame shape: {frame.shape}")  # Verify frame dimensions
else:
    print("Error: Failed to capture frame.")

# Release the camera
cap.release()

# Destroy any OpenCV windows (if you use any display windows)
cv2.destroyAllWindows()
