from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'tmp'  
SAVE_FOLDER = 'storage'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


os.makedirs(SAVE_FOLDER, exist_ok=True)

# Hàm xử lý ảnh
def process_image(file_path, output_folder):

    original_img = cv2.imread(file_path)

    gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    lab = cv2.cvtColor(original_img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_img = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(enhanced_img, cv2.COLOR_LAB2BGR)

    # Lưu các tệp ảnh xử lý
    gray_path = os.path.join(output_folder, 'gray.png')
    enhanced_path = os.path.join(output_folder, 'enhanced.png')
    cv2.imwrite(gray_path, gray_img)
    cv2.imwrite(enhanced_path, enhanced_img)

    return gray_path, enhanced_path

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    original_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(original_path)

    try:
       
        folder_name = os.path.splitext(filename)[0]
        output_folder = os.path.join(SAVE_FOLDER, folder_name)
        os.makedirs(output_folder, exist_ok=True)


        gray_path, enhanced_path = process_image(original_path, output_folder)


        saved_original_path = os.path.join(output_folder, filename)
        os.rename(original_path, saved_original_path)

        return jsonify({
            "message": "Files processed and saved successfully",
            "folder_path": output_folder,
            "files": {
                "original": saved_original_path,
                "gray": gray_path,
                "enhanced": enhanced_path,
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:

        if os.path.exists(original_path):
            os.remove(original_path)

if __name__ == '__main__':
    app.run(debug=True)
