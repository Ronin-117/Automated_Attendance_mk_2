from flask import Flask, request, render_template, redirect, url_for,send_file
from flask_socketio import SocketIO, emit
import cv2
import os
import time
from mtcnn import MTCNN
import pandas as pd
import face_recognition
import numpy as np
import pickle
from datetime import datetime
import threading
import logging

app = Flask(__name__)
socketio = SocketIO(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

processing_complete = False
FileName = ""

# Set up logging
logging.basicConfig(level=logging.DEBUG)

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

def process_attendance(file_path, base_url):
    global processing_complete, FileName
    frame_number = 0
    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(current_directory, "uploads", FileName)
    output_folder = os.path.join(current_directory, "Extracted_frames")
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Simulate a time-consuming task
    video = cv2.VideoCapture(video_path)
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
    video.release()
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global FileName
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
    
    FileName = file.filename
    # Save the file in the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Get the base URL
    base_url = request.host_url
    

    return render_template('results.html')

@app.route('/results')
def results():
    # Read the attendance file and pass the data to the template
    attendance_data = []
    if os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'r') as f:
            for line in f.readlines()[1:]:
                attendance_data.append(line.strip().split(','))

    return render_template('results.html', attendance_data=attendance_data)

@app.route('/get_csv')
def get_csv():
    # Path to your CSV file
    file_path = 'Attendance.csv'
    return send_file(file_path, mimetype='text/csv', as_attachment=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)