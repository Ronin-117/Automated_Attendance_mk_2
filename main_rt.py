import cv2
import os
from mtcnn import MTCNN
import pandas as pd
import face_recognition
import numpy as np
import pickle
from datetime import datetime


def load_encodings(file_path='encoding_passport_size_large.pkl'):
    with open(file_path, 'rb') as f:
        encodings = pickle.load(f)
    print('Encodings loaded from', file_path)
    return encodings

def markAttendance(name):
    file_path = 'Attendance.csv'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write('Name,Time\n')
    with open(file_path, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'{name},{dtString}\n')

# Load face encodings and names
path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

loaded_encodings = load_encodings('encoding_passport_size_large.pkl')



# Initialize the video capture
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # Use 0 for the default webcam
# Set the resolution to 3840x2160
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

fourcc= cv2.VideoWriter_fourcc(*'MJPG')
cap.set(cv2.CAP_PROP_FOURCC,fourcc)
cap.set(cv2.CAP_PROP_FORMAT,-1)

cropped_images = []

output_folder = 'detected'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_counter = 1

# Check if camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize the MTCNN detector
detector = MTCNN()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert the frame to RGB for MTCNN
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    faces = detector.detect_faces(frame_rgb)

    # Debug: print the face detection output
    print(faces)

    # Draw bounding boxes around the detected faces
    for face in faces:
        x, y, width, height = face['box']

        # Crop the image to the bounding box
        cropped_face = frame[y:y+height, x:x+width]

        # Resize the cropped image to 300x150
        resized_face = cv2.resize(cropped_face, (int(69*1),int(82*1)))
        #resized_face=cropped_face

        # Save the resized face to the 'detected' folder
        output_path = os.path.join(output_folder, f"face_{image_counter}.jpg")
        cv2.imwrite(output_path, resized_face)
        print(f"Saved: {output_path}")
        
        # Increment the image counter
        image_counter += 1
        
        # Store the cropped face in the list
        cropped_images.append(cropped_face)

        # Show the cropped face (optional)
        cv2.imshow("Cropped Face", cropped_face)

        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

    # Display the result
    cv2.imshow("Face Detection", frame)

    # Break the loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

new_encodings=[]
# Once the loop ends, process the cropped images for face recognition
for idx, cropped_image in enumerate(cropped_images):
    # Encode the cropped image
    face_encodings = face_recognition.face_encodings(cropped_image)
    if face_encodings:
        new_encodings.append(face_encodings[0])

    
for encodeFace in new_encodings:
                matches = face_recognition.compare_faces(loaded_encodings, encodeFace, tolerance=0.5)
                faceDis = face_recognition.face_distance(loaded_encodings, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    markAttendance(name)

# Release resources
cap.release()
cv2.destroyAllWindows()
