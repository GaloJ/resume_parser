from flask import Flask, request,jsonify, send_from_directory
from cv_pdf import parser_v1
from config import app
import time
import os

# Set a folder to save uploaded files
UPLOAD_FOLDER = 'uploads'  # You can change this to your desired upload directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'File not found'}), 400

        file = request.files['file']
        test_job_post = request.form['job_post']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if test_job_post == "":
            return jsonify({'error': 'Empty job post'}), 400

        # Save the file to the uploads directory

        current_time = time.strftime("%Y%m%d_%H%M%S")
        print(current_time)

        print(file.filename)
        timed_filename = f"{current_time}{file.filename}"

        file.save(os.path.join(UPLOAD_FOLDER, timed_filename))
        file_url = f'http://localhost:5000/files/{timed_filename}'

        resume_path = f"uploads/{timed_filename}"
        
        png_path, matchper, matchw, nomatchw = parser_v1(resume_path,test_job_post)

        png_url = f"http://localhost:5000/files/{png_path}"
        response_data = {'message': 'File uploaded successfully','file_url': png_url,
        'match_percentage':matchper, 'match_words':matchw, 'non_match_words':nomatchw }
        return jsonify(response_data), 200
    
    except Exception as e:
        print(f'Error occurred: {e}')
        return jsonify({'error': 'An error occurred during file upload'}), 500

# Endpoint to serve uploaded files
@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)