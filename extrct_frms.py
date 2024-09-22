import cv2
import os

# Function to extract every 20th frame
def extract_every_20th_frame(video_path, output_folder):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Capture the video from the file
    video = cv2.VideoCapture(video_path)

    # Check if video is opened successfully
    if not video.isOpened():
        print(f"Error opening video file: {video_path}")
        return
    
    # Initialize a frame count
    frame_number = 0

    # Loop until the end of the video
    while True:
        # Read frame-by-frame
        ret, frame = video.read()

        # If frame reading was successful
        if ret:
            # Check if this frame is the 20th, 40th, 60th, etc.
            if frame_number % 20 == 0:
                # Save the frame as an image file
                frame_name = os.path.join(output_folder, f"frame_{frame_number:05d}.jpg")
                cv2.imwrite(frame_name, frame)
                print(f"Saving {frame_name}")

            # Increment frame count
            frame_number += 1
        else:
            break

    # Release the video capture object
    video.release()
    print(f"Finished extracting frames")

# Example usage
video_path = "C:/Users/njne2/Desktop/Cuda_PWR/CREATIVE/Face_rec/iter2/uploads/1000156564.mp4"  
output_folder = "Extracted_frames"  

extract_every_20th_frame(video_path, output_folder)
