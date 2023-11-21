import base64
from urllib.parse import urlparse

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from PIL import Image

import os
from os.path import join, dirname, realpath
from proctor.proctoring import get_analysis, yolov3_model_v3_path

UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads/..')
app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
yolov3_model_v3_path("models/yolov3.weights")

# Define an API endpoint to receive the asset URL and save the image
@app.route('/image', methods=['POST'])
@cross_origin()
def save_image():
    img_data = request.form['data']

    binary_data = base64.b64decode(img_data)
    filename = "captured_image.png"  
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as f:
        f.write(binary_data)
    
    with open(filepath, 'rb') as f:
        base64_encoded_image = base64.b64encode(f.read()).decode('utf-8')

    proctorData = get_analysis(base64_encoded_image, "models/shape_predictor_68_face_landmarks.dat")
    if proctorData:
        data = {
        "status": 200,
        "message": "success",
        "payload": proctorData
        }
        return jsonify(data)
    data = {
        "status": 500,
        "message": "error",
        "payload": proctorData
    }
    
    return jsonify(data)

@app.route("/", methods=["GET"])
def hello():
    return jsonify("HELLO FROM PROCTORING API")

def separate_file_name_from_url(url):
    return os.path.basename(url).split('/')[-1]


# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
