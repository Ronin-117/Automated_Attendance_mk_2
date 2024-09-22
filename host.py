from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return '''
    <html>
    <body>
        <h1>Upload Video</h1>
        <form method="POST" enctype="multipart/form-data" action="/upload">
            <input type="file" name="file" accept="video/*">
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'

    # Save the file in the upload folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    
    return f"File {file.filename} uploaded successfully!"

if __name__ == '__main__':
    # Get the local IP of your laptop to allow access from mobile
    app.run(host='0.0.0.0', port=5000)
