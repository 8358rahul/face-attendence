from flask import Blueprint, jsonify, request
from deepface import DeepFace 
import os

verify_face_bp = Blueprint('verify_face_route', __name__)

# Directory to store temporary files
TEMP_DIR = "temp"

# Ensure the temp directory exists
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
@verify_face_bp.route('/', methods=['POST'])
def verify_face():
    try:
        # Validate that files are included in the request
        if 'img1' not in request.files or 'img2' not in request.files:
            return jsonify({"error": "Both img1 and img2 files are required"}), 400

        # Retrieve uploaded files
        img1 = request.files['img1']
        img2 = request.files['img2']

        # Validate the file types (optional but recommended)
        if not allowed_file(img1.filename) or not allowed_file(img2.filename):
            return jsonify({"error": "Invalid file type. Only .jpg and .png are supported"}), 400

        # Save the files temporarily
        img1_path = os.path.join(TEMP_DIR, secure_filename(img1.filename))
        img2_path = os.path.join(TEMP_DIR, secure_filename(img2.filename))
        img1.save(img1_path)
        img2.save(img2_path)

        # Perform face verification
        result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path, model_name="Facenet", detector_backend="mtcnn")

        # Cleanup temporary files
        cleanup_files([img1_path, img2_path])

           # Check match result
        if result["verified"]:
            return jsonify({
                "match_found": True,
                "distance": result["distance"],
                "similarity_model": result["model"]
            }), 200
        else:
            return jsonify({
                "match_found": False,
                "message": "The faces in the provided images do not match.",
                "distance": result["distance"],
                "similarity_model": result["model"]
            }), 200

    except Exception as e:
        # Handle unexpected errors and clean up temporary files
        if 'img1_path' in locals() and os.path.exists(img1_path):
            os.remove(img1_path)
        if 'img2_path' in locals() and os.path.exists(img2_path):
            os.remove(img2_path)
        return jsonify({"error": str(e)}), 500

def allowed_file(filename):
    """Validate if the uploaded file is of an allowed type"""
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def secure_filename(filename):
    """Generate a safe version of the filename"""
    return filename.replace(" ", "_").replace("/", "_").lower()

def cleanup_files(file_paths):
    """Remove temporary files"""
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)