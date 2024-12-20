from flask import Blueprint, jsonify, request
import os
from models.attendance import Attendance
from models.user import User
from db import db
from routes.helper import allowed_file,secure_filename,cleanup_files
from deepface import DeepFace 
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

TEMP_DIR = "temp"
@attendance_bp.route('/', methods=['POST'])
def mark_attendance():
    data = request.form
    photo = request.files.get('photo')
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email ID is required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 400
    if not photo:
        return jsonify({"error": "Profile image is required"}), 400
    if not allowed_file(photo.filename):
            return jsonify({"error": "Invalid file type. Only .jpg and .png are supported"}), 400
        
     # Save the uploaded photo temporarily
    temp_dir = TEMP_DIR
    os.makedirs(temp_dir, exist_ok=True)
    uploaded_photo_path = os.path.join(temp_dir, secure_filename(photo.filename))
    photo.save(uploaded_photo_path)
    
     # Path to the user's stored photo (assume it is stored with a full path in the `photo` field)
    stored_photo_path = user.photo
    if not os.path.exists(stored_photo_path):
        cleanup_files([uploaded_photo_path])
        return jsonify({"error": "Profile verification pending!"}), 500
    try:
        # Perform face verification
     
        result = DeepFace.verify(
            img1_path=stored_photo_path,
            img2_path=uploaded_photo_path,
            model_name="Facenet",
            detector_backend="mtcnn"
        )
        
        # Cleanup temporary file
        cleanup_files([uploaded_photo_path])
        
        # Check if the faces match 
        if not result["verified"]:
            return jsonify({
                    "success": False,
                    "message": "Face verification failed. The provided photo does not match the user's profile photo."
            }), 400


        # Record attendance
        today = datetime.now().date()
        check_in_time = datetime.now().time()
        attendance = Attendance.query.filter_by(user_id=user.id, date=today).first()

        if not attendance:
            attendance = Attendance(
                user_id=user.id,
                date=today,
                check_in_time=check_in_time,
                status="Present"
            )
            db.session.add(attendance)
        else:
            attendance.check_out_time = check_in_time
            attendance.status = "Present"

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Attendance recorded successfully",
            "attendance": {
                "userId": attendance.user_id,
                "date": str(attendance.date),  # Convert date to string
                "checkInTime": attendance.check_in_time.strftime('%H:%M:%S') if attendance.check_in_time else None,  # Convert time to string
                "checkOutTime": attendance.check_out_time.strftime('%H:%M:%S') if attendance.check_out_time else None,  # Convert time to string
                "status": attendance.status
        }
        }), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


@attendance_bp.route('/get_attendance/<email>', methods=['GET'])
def get_attendance(email):
    print("hello")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404

    attendances = Attendance.query.filter_by(user_id=user.id).all()
    return jsonify({
        "firstName": user.firstName,
        "lastName": user.lastName,
        "attendances": [
            {"date": att.date.strftime("%Y-%m-%d"), "status": att.status} for att in attendances
        ]
    })
