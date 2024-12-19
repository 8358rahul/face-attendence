from flask import Blueprint, jsonify, request
from models.attendance import Attendance
from models.user import User
from db import db

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/', methods=['POST'])
def mark_attendance():  
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404

    attendance = Attendance(user_id=user.id, ate=data['date'], status=data['status'])
    db.session.add(attendance)
    db.session.commit()
    return jsonify({"message": f"Attendance marked for {user.name}!"})

@attendance_bp.route('/get_attendance/<email>', methods=['GET'])
def get_attendance(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404

    attendances = Attendance.query.filter_by(user_id=user.id).all()
    return jsonify({
        "name": user.name,
        "attendances": [
            {"date": att.date.strftime("%Y-%m-%d"), "status": att.status} for att in attendances
        ]
    })
