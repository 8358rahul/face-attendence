from flask import Blueprint, jsonify, request
from models.user import User
from werkzeug.utils import secure_filename
import os
import shutil
from app import db
import uuid
from datetime import datetime
from routes.helper import allowed_file

users_bp = Blueprint('user_routes', __name__)

# Directory to store temporary files
TEMP_DIR = "temp"

# Ensure the temp directory exists
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'firstName': user.firstName,'lastName': user.lastName, 'email': user.email} for user in users])

@users_bp.route('/', methods=['POST'])
def create_user():
    try:
        # Retrieve Data
        data = request.form
        # Retrieve uploaded photo
        photo = request.files['photo']
         
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        
        if not first_name or not last_name or not email:
            return jsonify({"error": "Missing required user details"}), 400
        
        # Check for duplicate email
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400
        
        # Ensure photo is in the request files
        if 'photo' not in request.files:
            return jsonify({"error": "Profile Image required"}), 400

        # Validate the file type
        if not allowed_file(photo.filename):
            return jsonify({"error": "Invalid file type. Only .jpg and .png are supported"}), 400

        # Generate a unique filename
        file_extension = photo.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.{file_extension}"


        # Save the photo temporarily
        temp_photo_path = os.path.join(TEMP_DIR, unique_filename)
        photo.save(temp_photo_path )


        # Move photo to a permanent location
        permanent_photo_dir = os.path.join("uploads", "photos")
        os.makedirs(permanent_photo_dir, exist_ok=True)
        permanent_photo_path = os.path.join(permanent_photo_dir, unique_filename)
        shutil.move(temp_photo_path, permanent_photo_path)
       

        # Simulate saving to the database
        new_user = User(
        firstName=first_name,
        lastName=last_name,
        email=email,
        photo=permanent_photo_path 
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "user": {
                "id": new_user.id,
                "firstName": new_user.firstName,
                "lastName": new_user.lastName,
                "email": new_user.email,
                "photo": new_user.photo
            }
        }), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An unexpected error occurred"}), 500
    

